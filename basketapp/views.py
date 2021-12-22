from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from productsapp.models import Product


def index(request):
    content = {}
    return render(request, 'basketapp/basket.html', content)


def add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, pk):
    content = {}
    return render(request, 'basketapp/basket.html', content)