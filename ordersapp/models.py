from django.db import models
from django.utils.functional import cached_property

from django.conf import settings
from productsapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус',
                              max_length=3,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', db_index=True, default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    # кешируем один и тот же запрос
    @cached_property
    def get_items_cached(self):
        return self.orderitems.select_related()

    def get_total_quantity(self):
        # items = self.orderitems.select_related()
        items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        # items = self.orderitems.select_related()
        items = self.get_items_cached
        return len(items)

    def get_total_cost(self):
        # items = self.orderitems.select_related()
        items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    # Вместо двух методов «get_total_quantity()» и «get_total_cost()»
    # при использовании тега with в шаблоне будет один запрос
    def get_summary(self):
        # items = self.orderitems.select_related()
        items = self.get_items_cached
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


    # переопределяем метод, удаляющий объект, возвращаем на склад
    def delete(self):
        # возврат позиций на склад (тут кеш страшно ставить)
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        # деактивируем заказ, без настоящего удаления
        self.is_active = False
        self.save()


# описание в basketapp/models.py
class OrderItemQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(OrderItemQuerySet, self).delete(*args, **kwargs)

class OrderItem(models.Model):
    # перешли на сигналы
    # objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

    # # перешли на сигналы в ordersapp/views.py
    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()
