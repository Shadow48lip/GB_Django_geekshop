from django.urls import path, include
# from .views import productsapp
import productsapp.views as products

app_name = 'products'

urlpatterns = [
    # path('', productsapp),
    path('', products.index, name='index'),
    path('<int:pk>/', products.index, name='category'),
]