# -*- coding:utf-8 -*-

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from dcf.models import Item, Group, Profile


class BaseTestCase(TestCase):
    fixtures = [
        'section',
        'group'
    ]

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

        self.group = Group.objects.get(slug='new-cars')
        self.item = Item.objects.create(
            user=self.user,
            group=self.group,
            title='Tesla Model 3',
            description='Super new 2017 Tesla Model 3 electric Car',
            price=35000.00,
        )


class DCFTestCase(BaseTestCase):
    def test_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('robots'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('django.contrib.sitemaps.views.sitemap'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rss'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')

    def test_item_page(self):
        response = self.client.get(self.item.get_absolute_url())
        self.assertContains(response, self.item.title)

    def test_group_page(self):
        response = self.client.get(self.group.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        response = self.client.get('/this-is-wrong-path')
        self.assertContains(response, '404', status_code=404)

    def test_profile_update(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        response = self.client.get(reverse('profile'))
        self.assertContains(response, self.profile.phone)

        new_data = {'phone': '1111111111'}
        self.client.post(reverse('profile'), new_data)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, new_data['phone'])

    def test_item_search_by_title(self):
        response = self.client.get(reverse('search'), {'q': self.item.title})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_by_description(self):
        response = self.client.get(reverse('search'), {'q': self.item.description})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_by_group(self):
        response = self.client.get(reverse('search'), {'group': self.item.group.pk})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_not_found(self):
        response = self.client.get(reverse('search'), {'q': 'WRONG KEYWORDS'})
        self.assertNotContains(response, self.item.get_absolute_url())

    def test_user_can_add_item(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        self.assertTrue(self.profile.allow_add_item(), True)

        item_data = {
            'image_set-TOTAL_FORMS': 0,
            'image_set-INITIAL_FORMS': 0,
            'group': self.group.pk,
            'title': 'iPhone X',
            'description': 'New, Unlocked. Face ID',
            'price': 999,
            'is_active': True
        }
        response = self.client.post(reverse('item-new'), item_data, follow=True)
        self.assertContains(response, item_data['title'])
