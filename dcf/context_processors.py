# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def common_values(request):

    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    google_verification_id = getattr(settings, 'GOOGLE_SITE_VERIFICATION_ID', False)

    values = {}

    if not settings.DEBUG and ga_prop_id:
        values['GOOGLE_ANALYTICS_PROPERTY_ID'] = ga_prop_id

    if not settings.DEBUG and google_verification_id:
        values['GOOGLE_SITE_VERIFICATION_ID'] = google_verification_id

    values['settings'] = settings.DCF

    return values
