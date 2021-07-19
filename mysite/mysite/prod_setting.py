import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = '84xz4~A15HrFd*B5ec???9IetrvZXZq~ELH*UP5T4ACT0~La{Xou'
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']


STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'mysite/static')

]

DATABASES = {
    'default': {
        #

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'busel',
        'USER' : 'busel_admin',
        'PASSWORD' : 'masterAdminBusel#345',
        'HOST' : 'localhost',
        'PORT' : '5432',
    }
}