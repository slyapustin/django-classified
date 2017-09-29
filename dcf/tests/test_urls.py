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

        response = self.client.get(self.item.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.group.get_absolute_url())
        self.assertEqual(response.status_code, 200)

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

    def test_item_search(self):
        response = self.client.get(reverse('search'), {'q': self.item.title})
        self.assertContains(response, self.item.get_absolute_url())
