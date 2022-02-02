from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse

from django.core.mail import send_mail
from django.conf import settings

from authapp.models import ShopUser
from django.db import transaction


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    # ловим от декоратора @login_required куда пользователь шел
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    content = {'title': title, 'login_form': login_form, 'next': next}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


"""
Так как теперь изменения сохраняются в двух моделях, для обеспечения целостности данных применяем к контроллеру 
декоратор @transaction.atomic. Теперь, если произойдет ошибка записи данных в базу внутри контроллера, никакие 
данные вообще не записываются. 
"""


@login_required
@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form, }
    return render(request, 'authapp/edit.html', content)


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            # send e-mail
            if send_verify_mail(user):
                print('сообщение подтверждения умпешно отправлено')
            else:
                print('ошибка отправки сообщения')

            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def verify(request, email, activation_key):
    title = 'подтверждение'

    # Переделал условие. У нас E-mail не уникален и .get может вернуть более однной строки
    # нужно фильтровать еще и по по двум полям или только по activation_key
    try:
        user = ShopUser.objects.get(activation_key=activation_key)
        if user.email == email and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            print(f'OK activation user: {user}')
        else:
            print(f'error activation user: {user}')

        content = {'title': title}
        return render(request, 'authapp/verification.html', content)

    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'{user.first_name}, подтвердите свою учетную запись'

    message = f'Для подтверждения учетной записи "{user.username}" на сайте\
{settings.DOMAIN_NAME}\nперейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
