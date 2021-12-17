from django.shortcuts import render
from .models import ProductCategory


# Create your views here.
def index(request, pk=None):
    title = 'каталог'
    categories = ProductCategory.objects.all()

    # links_menu = [
    #     {'href': 'products/', 'name': 'все'},
    #     {'href': 'products_home/', 'name': 'дом'},
    #     {'href': 'products_office/', 'name': 'офис'},
    #     {'href': 'products_modern/', 'name': 'модерн'},
    #     {'href': 'products_classic/', 'name': 'классика'},
    # ]

    context = {
        'title': title,
        # 'links_menu': links_menu,
        'categories': categories,
        'pk': pk,
    }
    return render(request, 'productsapp/products.html', context=context)