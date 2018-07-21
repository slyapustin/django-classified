# -*- coding:utf-8 -*-
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed

from . import settings as dcf_settings
from .models import Item


class LatestItemFeed(Feed):
    # TODO Should return proper XML content type
    link = '/'
    description = dcf_settings.SITE_NAME

    def title(self):
        return Site.objects.get_current().name

    def items(self):
        return Item.active.order_by('-updated')[:dcf_settings.RSS_LIMIT]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
