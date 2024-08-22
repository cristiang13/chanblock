from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','chanblock.com','localhost','121.44.26.102']
STATICFILES_DIRS = 'static',
STATIC_ROOT= os.path.join(BASE_DIR, 'static')
