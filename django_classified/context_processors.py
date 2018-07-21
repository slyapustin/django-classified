# -*- coding:utf-8 -*-
from django.conf import settings

from . import settings as dcf_settings
from .models import Area


def common_values(request):
    return {
        'DCF': dcf_settings,
        'FACEBOOK_APP_ID': getattr(settings, 'FACEBOOK_APP_ID', ''),
        'GOOGLE_ANALYTICS_PROPERTY_ID': getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', ''),
        'GOOGLE_SITE_VERIFICATION_ID': getattr(settings, 'GOOGLE_SITE_VERIFICATION_ID', ''),
        'area_list': Area.objects.all(),
        'area': Area.get_for_request(request)
    }
