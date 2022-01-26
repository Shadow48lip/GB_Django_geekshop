from django.urls import path, include
# from .views import productsapp
import productsapp.views as products

app_name = 'productsapp'

urlpatterns = [
    # path('', productsapp),
    path('', products.index, name='index'),
    path('<int:pk>/', products.index, name='category'),
    path('<int:pk>/page/<int:page>/', products.index, name='page'),
    path('product/<int:pk>/', products.product, name='product'),
]