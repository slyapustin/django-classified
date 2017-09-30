# -*- coding:utf-8 -*-

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from dcf.models import Item, Group, Profile
from dcf.settings import DCF_ITEM_PER_USER_LIMIT


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
    def test_index_page(self):
        response = self.client.get(reverse('dcf:index'))
        self.assertContains(response, self.group.section.title)

    def test_pages(self):
        response = self.client.get(reverse('dcf:robots'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('dcf:search'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('dcf:sitemap'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('dcf:rss'))
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

    def test_profile_update(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        response = self.client.get(reverse('dcf:profile'))
        self.assertContains(response, self.profile.phone)

        new_data = {'phone': '1111111111'}
        self.client.post(reverse('dcf:profile'), new_data)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, new_data['phone'])

    def test_item_search_by_title(self):
        response = self.client.get(reverse('dcf:search'), {'q': self.item.title})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_by_description(self):
        response = self.client.get(reverse('dcf:search'), {'q': self.item.description})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_by_group(self):
        response = self.client.get(reverse('dcf:search'), {'group': self.item.group.pk})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_not_found(self):
        response = self.client.get(reverse('dcf:search'), {'q': 'WRONG KEYWORDS'})
        self.assertNotContains(response, self.item.get_absolute_url())

    def test_user_can_add_item(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        self.assertTrue(self.profile.allow_add_item(), True)

        response = self.client.get(reverse('dcf:item-new'))
        self.assertEqual(response.status_code, 200)

        with open('dcf/static/dcf/img/close.png', 'rb') as image_file:
            item_data = {
                'image_set-TOTAL_FORMS': 1,
                'image_set-INITIAL_FORMS': 3,
                'image_set-0-file': image_file,
                'image_set-0-id': '1',
                'group': self.group.pk,
                'title': 'iPhone X',
                'description': 'New, Unlocked. Face ID',
                'price': 999,
                'is_active': True
            }
            response = self.client.post(reverse('dcf:item-new'), item_data, follow=True)
            self.assertContains(response, item_data['title'])

    def test_user_can_update_item(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        self.assertEqual(self.user.item_set.count(), 1)

        response = self.client.get(reverse('dcf:item-edit', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)

        item_data = {
            'image_set-TOTAL_FORMS': 0,
            'image_set-INITIAL_FORMS': 0,
            'group': self.group.pk,
            'title': 'iPhone X',
            'description': 'New, Unlocked. Face ID',
            'price': 999,
            'is_active': True
        }
        response = self.client.post(reverse('dcf:item-edit', kwargs={'pk': self.item.pk}), item_data, follow=True)
        self.assertEqual(self.user.item_set.count(), 1)
        self.assertContains(response, item_data['title'])
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, item_data['title'])

    def test_user_can_not_add_more_than_allowed_items(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        self.assertTrue(self.profile.allow_add_item())

        item_data = {
            'image_set-TOTAL_FORMS': 0,
            'image_set-INITIAL_FORMS': 0,
            'group': self.group.pk,
            'title': 'iPhone X',
            'description': 'New, Unlocked. Face ID',
            'price': 999,
            'is_active': True
        }
        for i in range(self.user.item_set.count(), DCF_ITEM_PER_USER_LIMIT + 10):
            self.client.post(reverse('dcf:item-new'), item_data)

        self.assertFalse(self.profile.allow_add_item())
        self.assertEqual(self.user.item_set.count(), DCF_ITEM_PER_USER_LIMIT)

    def test_user_can_delete_item(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        self.assertEqual(Item.objects.all().count(), 1)
        response = self.client.get(reverse('dcf:my-delete', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)

        self.client.post(reverse('dcf:my-delete', kwargs={'pk': self.item.pk}))
        self.assertEqual(Item.objects.all().count(), 0)

    def test_user_can_view_own_items(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        self.assertEqual(Item.objects.all().count(), 1)
        response = self.client.get(reverse('dcf:user-items'))
        self.assertContains(response, self.item.get_absolute_url())
