from django.shortcuts import render

from basketapp.models import Basket
from productsapp.models import Product

# Create your views here.
def index(request):
    title = 'главная'
    products = Product.objects.all()[:4]

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    context = {
        'title': title,
        'products': products,
        'basket': basket,
    }
    return render(request, 'mainapp/index.html', context=context)


def contacts(request):
    title = 'контакты'

    context = {
        'title': title,
    }
    return render(request, 'mainapp/contacts.html', context=context)