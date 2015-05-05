# -*- coding:utf-8 -*-
from django.conf import settings


def common_values(request):

    data = {}

    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    ya_metrika_prop_id = getattr(settings, 'YANDEX_METRIKA_PROPERTY_ID', False)


    if not settings.DEBUG and ga_prop_id:
        data['GOOGLE_ANALYTICS_PROPERTY_ID'] = ga_prop_id

    if not settings.DEBUG and ya_metrika_prop_id:
        data['YANDEX_METRIKA_PROPERTY_ID'] = ya_metrika_prop_id

    data['settings'] = settings.DCF

    return data