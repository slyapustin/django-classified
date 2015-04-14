# -*- coding:utf-8 -*-
from django.conf import settings


def common_values(request):

    data = {
        'settings': settings.DCF
    }

    return data