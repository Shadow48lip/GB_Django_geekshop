from django.shortcuts import render

from productsapp.models import Product
from productsapp.views import get_products


def index(request):
    title = 'главная'
    # products = Product.objects.filter(is_active=True, category__is_active=True)[:3]
    products = get_products()[:3]

    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'mainapp/index.html', context=context)


def contacts(request):
    title = 'контакты'

    context = {
        'title': title,
    }
    return render(request, 'mainapp/contacts.html', context=context)
