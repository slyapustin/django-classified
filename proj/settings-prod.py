# -*- coding:utf-8 -*-
from settings import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.craiglists.ru', ]

ADMINS = (
    ('Admin', 'inoks@mail.ru'),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SECRET_KEY = 'sfdfsdfksd;f;sdkf;lskdf;ksd;lfk;sdkf;lksd;lfksd;lfk;lsdkfl;skdf;lksdl;kfl;wekrwer'

TIME_ZONE = 'Europe/Kaliningrad'

SOCIAL_AUTH_FACEBOOK_KEY = '969556519755162'
SOCIAL_AUTH_FACEBOOK_SECRET = '77c90be18aa69bd4f7c1146ae8dc2b2a'

DCF['SITE_NAME'] = 'Demo DCF Site'

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-568125-13'