# -*- coding:utf-8 -*-
from django.conf import settings

from . import settings as dcf_settings


def common_values(request):
    return {
        'DCF_CURRENCY': dcf_settings.DCF_CURRENCY,
        'DCF_DISPLAY_CREDITS': dcf_settings.DCF_DISPLAY_CREDITS,
        'DCF_LOGIN_TO_CONTACT': dcf_settings.DCF_LOGIN_TO_CONTACT,
        'DCF_SITE_DESCRIPTION': dcf_settings.DCF_SITE_DESCRIPTION,
        'DCF_SITE_NAME': dcf_settings.DCF_SITE_NAME,
        'FACEBOOK_APP_ID': getattr(settings, 'FACEBOOK_APP_ID', ''),
        'GOOGLE_ANALYTICS_PROPERTY_ID': getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', ''),
        'GOOGLE_SITE_VERIFICATION_ID': getattr(settings, 'GOOGLE_SITE_VERIFICATION_ID', ''),
    }
