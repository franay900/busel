import os
from pathlib import Path
import pymysql

pymysql.install_as_MySQLdb()
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '84xz4~A15HrFd*B5ec???9IetrvZXZq~ELH*UP5T4ACT0~La{Xou'
DEBUG = False




STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'mysite/static')

]




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'buselxyz_busel',
        'USER': 'buselxyz_admin',
        'PASSWORD': '9[2G8BvLYAv',
        'HOST': 'localhost',
        'Port': '3306'
    }
}