import random
from basketapp.models import Basket
from .models import ProductCategory, Product
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.filter(is_active=True, category__is_active=True)

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True,
                                           category__is_active=True).exclude(pk=hot_product.pk)[:3]

    return same_products


def index(request, pk=None, page=1):
    title = 'продукты'

    basket = get_basket(request.user)
    # links_menu = ProductCategory.objects.all()
    links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True). \
                order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            'basket': basket,
        }
        # return render(request, 'productsapp/products_list.html', content)

    else:
        hot_product = get_hot_product()
        same_products = get_same_products(hot_product)

        content = {
            'title': title,
            'links_menu': links_menu,
            'same_products': same_products,
            'hot_product': hot_product,
            'basket': basket,
        }

    return render(request, 'productsapp/products.html', content)


def product(request, pk):
    title = 'продукт'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'productsapp/product.html', content)
