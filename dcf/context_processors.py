# -*- coding:utf-8 -*-
from django.conf import settings


def common_values(request):

    values = {
        'GOOGLE_ANALYTICS_PROPERTY_ID': getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', ''),
        'GOOGLE_SITE_VERIFICATION_ID': getattr(settings, 'GOOGLE_SITE_VERIFICATION_ID', ''),
        'settings': settings.DCF
    }

    return values
