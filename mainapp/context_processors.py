from basketapp.models import Basket

# Служит для добавление в сепссию корзины сразу на все страницы. Подключается в settings
def basket(request):
    # print(f'context processor basket works')
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    return {
        'basket': basket,
    }
