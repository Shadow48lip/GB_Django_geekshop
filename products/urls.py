from django.urls import path, include
# from .views import products
import products.views as products

urlpatterns = [
    # path('', products),
    path('', products.index),
]