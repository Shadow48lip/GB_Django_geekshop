from django.shortcuts import render


# Create your views here.
def index(request):
    title = 'магазин'

    context = {
        'title': title,
    }
    return render(request, 'mainapp/index.html', context=context)


def contacts(request):
    title = 'контакты'

    context = {
        'title': title,
    }
    return render(request, 'mainapp/contacts.html', context=context)