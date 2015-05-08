# -*- coding:utf-8 -*-

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from dcf.models import Item, Group, Section


class GenericViewTestCase(TestCase):

    def setUp(self):

        self.section = Section.objects.create(title=u'Cars')
        self.group = Group.objects.create(title=u'Electric Cars', section=self.section)
        self.user = get_user_model().objects.create(username="test")
        self.item = Item.objects.create(user=self.user, group=self.group, title=u'Tesla S',
                                        description=u'Super new 2015 Tesla S electric Car',
                                        price=79000.00, phone='1-121-12-90')


class TestUrls(GenericViewTestCase):

    def test_pages(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('robots'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('sitemap'))
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