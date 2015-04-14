# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.conf import settings

from .models import Item


class LatestItemFeed(Feed):

    # TODO Should return proper XML content type
    title = Site.objects.get_current().name
    link = '/'
    description = u'%s updates' % settings.DCF['SITE_NAME']

    def items(self):

        return Item.objects.all().order_by('-updated')[:settings.DCF['RSS_LIMIT']]

    def item_title(self, item):

        return item.get_title()

    def item_description(self, item):

        return item.description[:200]