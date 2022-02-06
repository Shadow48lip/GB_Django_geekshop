from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from productsapp.models import Product


# В Django работа с QuerySet возможна через менеджер модели. Он сработет при массовом удалении по .filter(), а вот
# переопределенный метод .delete внутри модели Basket сработает только при удалении конкретной строки.
class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    # перешли на сигналы
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    # кешируем запросы
    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def product_cost(self):
        """return cost of all products this type"""
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        """return total quantity for user"""
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        """return total cost for user"""
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    # ИСПОЛЬЗУЕМ СИГНАЛЫ, а не этот вариант в ordersapp/views.py
    # # срабатывает только на построчное удаление, иначе работает BasketQuerySet
    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()
    #
    # # переопределяем метод, сохранения объекта
    # def save(self, *args, **kwargs):
    #     # если мы редактируем уже существующую запись - необходимо количество оставшихся
    #     # товаров изменить на разницу между прежним и новым значением в заказе (корзине)
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)
