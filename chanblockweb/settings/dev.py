from .base import *
import os



# ALLOWED_HOSTS = ['www.chanblock.com','chanblock.com']
# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS =['www.chanblock.com' ,'chanblock.com','121.44.26.102','localhost']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_SCHEME', 'https')
SECURE_SSL_REDIRECT = TRUE

STATIC_ROOT= 'static'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
