from django.urls import path, include
import basketapp.views as basket

app_name = 'basketapp'

urlpatterns = [
    path('', basket.index, name='index'),
    path('add/<int:pk>/', basket.add, name='add'),
    path('remove/<int:pk>)/', basket.remove, name='remove'),
]