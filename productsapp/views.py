import random
from .models import ProductCategory, Product
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page


# cache functions
def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, \
                                              category__is_active=True).select_related('category')
            cache.set(key, products)
            # print('set cache')
        # else:
        #     print('from cache')
        return products
    else:
        return Product.objects.filter(is_active=True, \
                                      category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, \
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, \
                                      category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, \
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, \
                                      category__is_active=True).order_by('price')


# old functions
def get_hot_product():
    # products = Product.objects.filter(is_active=True, category__is_active=True)
    products = get_products()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True,
                                           category__is_active=True).exclude(pk=hot_product.pk)[:3]

    return same_products


# кеширование контроллеров удобно так же производить в urls.py
@cache_page(60)
def index(request, pk=None, page=1):
    title = 'продукты'

    # links_menu = ProductCategory.objects.filter(is_active=True)
    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            # products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price'). \
            #     select_related()
            products = get_products_orederd_by_price()
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            category = get_category(pk)
            # products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True). \
            #     order_by('price')
            products = get_products_in_category_orederd_by_price(pk)

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
        }

    return render(request, 'productsapp/products.html', content)


def product(request, pk):
    title = 'продукт'

    content = {
        'title': title,
        # 'links_menu': ProductCategory.objects.all(),
        'links_menu': get_links_menu(),
        # 'product': get_object_or_404(Product, pk=pk),
        'product': get_product(pk),
    }

    return render(request, 'productsapp/product.html', content)
