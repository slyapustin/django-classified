# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clear entire cache'

    def handle(self, *args, **options):
        from django.core.cache import cache
        cache.clear()
