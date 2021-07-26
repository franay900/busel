import os
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '84xz44(&t+k=#dkwpdn_z92x8e07p4r07&x^0j_@sv1mhg54_&'
DEBUG = True

ALLOWED_HOSTS = []


STATIC_URL = '/static/'


DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'busel',
        'USER' : 'sadmin',
        'PASSWORD' : 'asszxx228',
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}

