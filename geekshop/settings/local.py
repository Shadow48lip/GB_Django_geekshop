"""
# Running django for local development
$ ./manage.py runserver 0:8000 --settings=geekshop.settings.local

"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# Список хостов/доменов, для которых может работать текущий сайт.
# https://djbook.ru/rel1.7/ref/settings.html
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# E-mail
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = env('EMAIL_PORT')

# Для формирования почтового сообщения
DEFAULT_FROM_EMAIL = 'noreply@geekshop.local'
DOMAIN_NAME = 'http://localhost:8000'