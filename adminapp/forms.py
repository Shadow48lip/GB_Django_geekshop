from django import forms
from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from productsapp.models import ProductCategory, Product


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(forms.ModelForm):
    # Виртуальное поле, его нет в БД. Не сохраняется в БД (required) и задаем имя (label)
    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        # fields = '__all__'
        exclude = ()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'description' and field.widget.input_type == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'description' and field.widget.input_type == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

