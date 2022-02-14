from django.core.management.base import BaseCommand

from ordersapp.models import OrderItem
from productsapp.models import Product
from django.db import connection
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from adminapp.views import db_profile_by_type
from datetime import timedelta

"""
Давайте теперь проверим свое понимание работы Django-ORM - сколько запросов получим, для закомментированной ранее команды: 
print(test_products)

Правильный ответ: по запросу на каждый продукт плюс один. Почему? Из-за нашей реализации метода «__str__()» модели Product:
return f"{self.name} ({self.category.name})"

Второй вопрос: как уменьшить число запросов? Правильный ответ: использовать метод «.select_related()» - получим всего 
один запрос. Также в качестве альтернативы можете попробовать убрать вывод имени категории в методе «__str__()» модели 
Product. Тоже получите один запрос.
"""

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         test_products = Product.objects.filter(
#             Q(category__name='Офис') |
#             Q(category__name='Модерн')
#         ).select_related()
#         # из-за «__str__()» модели Product (там идет запрос имени категории) лучше использовать select_related
#         # даст 1 запрос вместо 4
#
#         print(len(test_products))
#         # print(test_products)
#
#         db_profile_by_type('learn db', '', connection.queries)


"""
* при оплате заказа в течение 12 часов - скидка 30%; 
* при оплате заказа в течение суток - скидка 15%, 
* на остальные товары - скидка 5%. 
Выведем данные о величине скидки на каждый элемент заказа с учетом акции следующим образом. Сначала выводим позиции, 
которые попали под первую акцию в порядке увеличения выгоды. Затем позиции, которые попали под вторую акцию в порядке
 уменьшения выгоды. Потом - остальные позиции, снова в порядке увеличения выгоды. Чередование можно реализовать и для 
 большего количества предложений. Таким образом получим своего рода волны, по которым можно найти самые выгодные 
 товары на границах акций.

Чтобы сэкономить время и не создавать новых атрибутов модели, будем считать датой оплаты заказа значение 
его атрибута «updated».
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)

        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
                              Q(order__updated__lte=F('order__created') + action_2__time_delta)

        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition,
                               then=F('product__price') * F('quantity') * action_1__discount)

        action_2__price = When(action_2__condition,
                               then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        """
        Далее выполняем цепочку методов в менеджере модели элемента заказа OrderItem. При помощи метода «.annotate()» 
        добавляем поля аннотаций «action_order» и «total_price» к каждому объекту QuerySet. Сортируем результаты по этим 
        полям и подгружаем данные связанных моделей для уменьшения количества запросов.
        """

        test_orderss = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        for orderitem in test_orderss:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:\
                   {orderitem.product.name:18}: скидка\
                   {abs(orderitem.total_price):7.2f} руб. | \
                   {orderitem.order.updated - orderitem.order.created}')

        # db_profile_by_type('learn db', '', connection.queries)
