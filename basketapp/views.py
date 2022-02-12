from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import F
from basketapp.models import Basket
from productsapp.models import Product


@login_required
def index(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

    content = {
        'title': title,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/basket.html', content)

@login_required
def add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if basket:
        basket.quantity = F('quantity') + 1
    else:
        basket = Basket(user=request.user, product=product)
        basket.quantity = 1

    # basket.quantity += 1
    basket.save()

    # если пришли с формы авторизации после редиректа туда как неавторизованного
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})