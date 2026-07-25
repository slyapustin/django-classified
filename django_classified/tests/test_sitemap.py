from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from django_classified.models import Group, Item, Profile, Section


class SitemapTestCase(TestCase):
    """Sitemap coverage: Item entries plus the Group (category) entries."""

    def setUp(self):
        self.username = 'John'
        self.password = 'summer'
        self.email = 'john@example.com'
        self.user = get_user_model().objects.create_user(
            self.username,
            self.email,
            self.password
        )
        self.profile = Profile.get_or_create_for_user(self.user)
        self.profile.phone = '0123456789'
        self.profile.save()

        self.section = Section.objects.create(
            title='Cars'
        )

        self.group = Group.objects.create(
            slug='new-cars',
            title='New cars',
            section=self.section
        )
        self.item = Item.objects.create(
            user=self.user,
            group=self.group,
            title='Tesla Model 3',
            description='Super new 2017 Tesla Model 3 electric Car',
            price=35000.00,
        )

        self.inactive_item = Item.objects.create(
            user=self.user,
            group=self.group,
            title='Sold Tesla Model S',
            description='No longer available',
            price=1.00,
            is_active=False,
        )

        # A group with no active items - should not show up in the sitemap,
        # an empty category page is a thin/soft-404 page.
        self.empty_group = Group.objects.create(
            slug='empty-group',
            title='Empty group',
            section=self.section,
        )

    def test_sitemap_returns_200(self):
        response = self.client.get(reverse('django_classified:sitemap'))
        self.assertEqual(response.status_code, 200)

    def test_active_item_url_in_sitemap(self):
        response = self.client.get(reverse('django_classified:sitemap'))
        self.assertContains(response, self.item.get_absolute_url())

    def test_inactive_item_not_in_sitemap(self):
        response = self.client.get(reverse('django_classified:sitemap'))
        self.assertNotContains(response, self.inactive_item.get_absolute_url())

    def test_group_with_active_items_in_sitemap(self):
        response = self.client.get(reverse('django_classified:sitemap'))
        self.assertContains(response, self.group.get_absolute_url())

    def test_group_without_active_items_not_in_sitemap(self):
        response = self.client.get(reverse('django_classified:sitemap'))
        self.assertNotContains(response, self.empty_group.get_absolute_url())

    def test_group_entry_has_lastmod(self):
        response = self.client.get(reverse('django_classified:sitemap'))
        content = response.content.decode()

        group_url = self.group.get_absolute_url()
        self.assertIn(group_url, content)

        # Pull out the <url>...</url> block containing the group location,
        # so we check the lastmod that belongs to it (not some other entry).
        block_start = content.rindex('<url>', 0, content.index(group_url))
        block_end = content.index('</url>', content.index(group_url))
        url_block = content[block_start:block_end]

        self.assertIn('<lastmod>', url_block)
        self.assertIn(self.item.updated.strftime('%Y-%m-%d'), url_block)

    def test_sitemap_query_count_is_bounded(self):
        url = reverse('django_classified:sitemap')

        # Warm up caches that are unrelated to the sitemap itself (notably
        # django.contrib.sites' Site.objects.get_current() cache) so the
        # assertion below only measures the sitemap's own queries.
        self.client.get(url)

        # Expect 4 queries total: for each of the two registered sitemaps
        # (Item, Group) the paginator issues one COUNT(*) query and one
        # SELECT query for the page of results. The Group query carries the
        # lastmod as a Max(...) annotation computed in a single query, so
        # this stays flat no matter how many groups/items exist - it locks
        # in that lastmod is annotated, not fetched per-row (no N+1).
        with self.assertNumQueries(4):
            self.client.get(url)
