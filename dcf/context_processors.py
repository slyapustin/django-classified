# -*- coding:utf-8 -*-
from django.conf import settings


def common_values(request):

    values = {
        'DCF_DISPLAY_CREDITS': settings.DCF_DISPLAY_CREDITS,
        'DCF_LOGIN_TO_CONTACT': settings.DCF_LOGIN_TO_CONTACT,
        'DCF_SITE_DESCRIPTION': settings.DCF_SITE_DESCRIPTION,
        'DCF_SITE_NAME': settings.DCF_SITE_NAME,
        'GOOGLE_ANALYTICS_PROPERTY_ID': settings.GOOGLE_ANALYTICS_PROPERTY_ID,
        'GOOGLE_SITE_VERIFICATION_ID': settings.GOOGLE_SITE_VERIFICATION_ID,
    }

    return values
