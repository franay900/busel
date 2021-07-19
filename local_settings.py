import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '84xz44(&t+k=#dkwpdn_z92x8e07p4r07&x^0j_@sv1mhg54_&'
DEBUG = True

ALLOWED_HOSTS = []


STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'mysite/static')

]
