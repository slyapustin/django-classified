from django.contrib.sitemaps import Sitemap
from django.conf import settings
from models import Item


class ItemSitemap(Sitemap):
    def items(self):
        return Item.objects.all()[:settings.DCF['SITEMAP_LIMIT']]

sitemaps_dict = {
    'Item': ItemSitemap,
    }