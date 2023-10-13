import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = '84xz4~A15HrFd*B5ec???9IetrvZXZq~ELH*UP5T4ACT0~La{Xou'
DEBUG = False




STATIC_ROOT=os.path.join(BASE_DIR,'/home/c/cb44146/public_html/static')


STATIC_URL = 'static/'
# STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')

]

MEDIA_ROOT=os.path.join(BASE_DIR,'/home/c/cb44146/public_html/media')
MEDIA_URL='/media/'

DATABASES = {
    'default': {
        #

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cb44146_busel',
        'USER' : 'cb44146_busel',
        'PASSWORD' : 'Tde8vhsi',
        'HOST' : 'localhost',
        'PORT' : '5432',
    }
}