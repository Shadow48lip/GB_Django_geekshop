from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')

def contacts(request):
    return render(request, 'mainapp/contacts.html')