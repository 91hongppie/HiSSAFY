from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', 'as1ix)g9coqp1f-5*2*r7vf0=22myzqo&g@*4q(dox*s$yri4o')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# use this when mysql is the basic db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ai',
        'USER': 'root',
        'PASSWORD': '1324adsf',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
