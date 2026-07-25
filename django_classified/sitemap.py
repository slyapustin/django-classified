from django.contrib.sitemaps import Sitemap
from django.db.models import Count, Max, Q

from . import settings as dcf_settings
from .models import Group, Item


class ItemSitemap(Sitemap):
    def changefreq(self, obj):
        return 'weekly'

    def lastmod(self, obj):
        return obj.updated

    def items(self):
        return Item.active.all()[:dcf_settings.SITEMAP_LIMIT]


class GroupSitemap(Sitemap):
    priority = 0.7

    def changefreq(self, obj):
        return 'daily'

    def lastmod(self, obj):
        # Read from the annotation added in items() - avoids an N+1 query
        # (one extra query per group) across the whole sitemap.
        return obj.lastmod

    def items(self):
        # Only list categories that actually have active items, an empty
        # category page is a thin/soft-404 page and shouldn't be submitted.
        # order_by() is explicit because the annotations below add a GROUP
        # BY, which makes Group's default Meta.ordering not apply, and
        # Django's paginator warns about unordered querysets otherwise.
        return Group.objects.annotate(
            active_count=Count('item', filter=Q(item__is_active=True)),
            lastmod=Max('item__updated', filter=Q(item__is_active=True)),
        ).filter(active_count__gt=0).order_by(
            'section__title', 'title'
        )[:dcf_settings.SITEMAP_LIMIT]


sitemaps_dict = {
    'Item': ItemSitemap,
    'Group': GroupSitemap,
}
