from django.test import TestCase
from django.test.client import Client
from productsapp.models import Product, ProductCategory
from django.core.management import call_command


# Обязательно выключаем режим отладки в файле настроек проекта перед запуском тестирования
# python manage.py dumpdata -e=contenttypes -e=auth -o test_db.json
# python manage.py dumpdata --natural-foreign --natural-primary --indent 2 -e contenttypes -e auth.Permission -e sessions > test_db.json


class TestMainappSmoke(TestCase):
    def setUp(self):
        # очистка базы
        call_command('flush', '--noinput')
        # аналог python manage.py loaddata test_db.json
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

        # если не включен memcached, то этот тест падает
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    # Так как разные базы данных по-разному работают с индексами при создании новых элементов - добавили в метод
    # «.tearDown()», выполняющийся всегда по завершении тестов в классе, команду сброса индексов:
    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp', 'productsapp')


