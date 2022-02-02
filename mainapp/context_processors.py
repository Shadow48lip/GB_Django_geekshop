from basketapp.models import Basket

# Служит для добавление в сессию корзины сразу на все страницы. Подключается в settings
def basket(request):
    # print(f'context processor basket works')
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).select_related()


    return {
        'basket': basket,
    }
