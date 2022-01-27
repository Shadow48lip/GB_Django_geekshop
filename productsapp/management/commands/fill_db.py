from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from productsapp.models import ProductCategory, Product
# from django.contrib.auth.models import User

import json, os

JSON_PATH = 'productsapp/json'

# python manage.py dumpdata  productsapp.ProductCategory productsapp.Product > dump.json

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)

# Заполняет новую базу начальными значениями
class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_id = product["category"]
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(pk=category_id)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        ShopUser.objects.all().delete()
        # super_user = User.objects.create_superuser('admin', 'django@geekshop.local', 'admin')
        super_user = ShopUser.objects.create_superuser('admin', 'django@geekshop.local', 'admin', age=30)