from django.urls import path, include
# from .views import productsapp
import productsapp.views as products

urlpatterns = [
    # path('', productsapp),
    path('', products.index),
]