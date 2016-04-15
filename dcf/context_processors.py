# -*- coding:utf-8 -*-
from django.conf import settings


def common_values(request):

    values = {
        'GOOGLE_ANALYTICS_PROPERTY_ID': getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', ''),
        'GOOGLE_SITE_VERIFICATION_ID': getattr(settings, 'GOOGLE_SITE_VERIFICATION_ID', ''),
        'DCF_SITE_NAME': settings.DCF_SITE_NAME,
        'DCF_SITE_DESCRIPTION': settings.DCF_SITE_DESCRIPTION,
        'DCF_LOGIN_TO_CONTACT': settings.DCF_LOGIN_TO_CONTACT,
    }

    return values
