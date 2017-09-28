# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import ugettext as _

from dcf.models import Item


class LatestItemFeed(Feed):
    # TODO Should return proper XML content type
    link = '/'
    description = _(u'%s updates' % settings.DCF_SITE_NAME)

    def title(self):
        return Site.objects.get_current().name

    def items(self):
        return Item.objects.all().order_by('-updated')[:settings.DCF_RSS_LIMIT]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description[:200]
