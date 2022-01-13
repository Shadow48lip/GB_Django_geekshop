from django.shortcuts import render

from productsapp.models import Product


def index(request):
    title = 'главная'
    products = Product.objects.all()[:4]

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
