from django.db.models import F
from django.shortcuts import render

from basketapp.models import Basket
from .models import ProductCategory, Product
from django.shortcuts import get_object_or_404


def index(request, pk=None):
    title = 'продукты'

    # basket = []
    basket_detail = {}
    if request.user.is_authenticated:
        # basket = Basket.objects.filter(user=request.user)
        basket_detail = Basket.objects.annotate(f_price=F('quantity') * F('product__price'))

        sum_price = 0
        sum_quantity = 0
        for line in basket_detail:
            sum_price += line.f_price
            sum_quantity += line.quantity

        basket_detail = {
            'sum_price': sum_price,
            'sum_quantity': sum_quantity,
        }


    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            category = {'name': 'все'}
            products = Product.objects.all().order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            # 'basket': basket,
            'basket_detail': basket_detail,
        }
        # return render(request, 'productsapp/products_list.html', content)

    else:
        same_products = Product.objects.all()[3:5]

        content = {
            'title': title,
            'links_menu': links_menu,
            'same_products': same_products,
            # 'basket': basket,
            'basket_detail': basket_detail,
        }

    return render(request, 'productsapp/products.html', content)
