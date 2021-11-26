from pathlib import Path
from datetime import timedelta
import os


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 't^p9hhd6%^jkdfhjk&ujflku646%632^^hxvkj)*^%jkhit2@pl4^rjn4w($r%#6rd!'

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "172.25.30.20"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'routesheet',
        'USER': 'hanuman',
        'PASSWORD': 'Olo$21FG!',
        'HOST':'localhost',
        'PORT': '5432',
    }
}

#STATIC_DIR = os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = [STATIC_DIR]
#STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')