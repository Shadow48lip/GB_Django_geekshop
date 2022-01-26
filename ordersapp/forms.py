from django import forms
from ordersapp.models import Order, OrderItem
from productsapp.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    # Виртуальное поле, его нет в БД. Не сохраняется в БД (required) и задаем имя (label)
    price = forms.CharField(label='цена', required=False)

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        #Отфильтровать продукты только с положительным остатком на складе + сортировка
        self.fields['product'].queryset = Product.objects.filter(is_active=True, quantity__gte=1).\
            order_by('category', 'name')
