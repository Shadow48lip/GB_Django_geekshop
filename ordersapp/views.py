from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.db.models import F

from django.forms import inlineformset_factory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm
from productsapp.models import Product

# приемник сигналов «receiver»
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


# <имя класса>_list.html
class OrderList(ListView):
    model = Order

    extra_context = {'title': 'заказы/список'}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    # только залогиненые могут сюда попасть
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


# <имя класса>_form.html
class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')
    extra_context = {'title': 'заказ/создание'}

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        """
        Необходимо обеспечить создание элементов заказа одновременно с самим заказом. По сути, каждый элемент заказа 
        должен создаваться на отдельной форме, для этого нам потребуется набор форм Django FormSets, связанных с 
        родительским классом (в нашем случае это заказ «Order», а не простой, на базе класса «OrderItem»). В Django это
        класс «InlineFormSet» (формы на основе моделей). Для его создания воспользуемся методом 
        «inlineformset_factory()» из модуля «django.forms».
        Первый позиционный аргумент - родительский класс, второй - класс, на основе которого будет создаваться набор 
        форм класса, указанного в именованном аргументе «form=OrderItemForm». Аргумент «extra» позволяет задать 
        количество новых форм в наборе
        """
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


# <имя класса>_form.html
class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')
    extra_context = {'title': 'заказ/редактирование'}

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            # для оптимизации прописываем применение select_related() в запрос
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            # form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


# <имя класса>_confirm_delete.html
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


# <имя класса>_detail.html
class OrderRead(DetailView):
    model = Order
    extra_context = {'title': 'заказ/просмотр'}


# изменения статуса заказа
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


# запрос цены для позиции товара в заказе
def get_item_price(request, pk):
    if request.is_ajax():
        product = get_object_or_404(Product, pk=pk)
        return JsonResponse({'price': product.price})
    return JsonResponse({'price': 0})


# СИГНАЛЫ
# функции при сохранении и удалении объектов моделей «Basket» и «OrderItem» через сигналы (декоратор @receiver)
# «sender» - класс отправителя;
# «update_fields» - имена обновляемых полей;
# «instance» - сам обновляемый объект
@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    # непонятно зачем вообще нужен это if. всегда прилетает None!
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            # тут падает при loaddata
            if sender.get_item(instance.pk) is not None:
                instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            # instance.product.quantity -= instance.quantity
            instance.product.quantity = F('quantity') - instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    # instance.product.quantity += instance.quantity
    instance.product.quantity = F('quantity') + instance.quantity
    instance.product.save()
    print('delete')
