# -*- coding:utf-8 -*-

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from dcf.models import Item, Group, Section


class ApiTestCase(APITestCase):

    def setUp(self):

        self.section = Section.objects.create(title=u'TestSection')
        self.group = Group.objects.create(
            title=u'TestGroup',
            section=self.section
        )
        self.user1 = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.user2 = get_user_model().objects.create(username=u'username2')
        self.item1 = Item.objects.create(
            user=self.user1,
            group=self.group,
            title=u'testitem1',
            description=u'test descr',
            price=1000.00,
            phone='8-800-9000-900'
        )
        self.item2 = Item.objects.create(
            user=self.user2,
            group=self.group,
            title=u'testitem2',
            description=u'test descr',
            price=2000.00,
            phone='8-800-7800-123'
        )

    def test_groups_api(self):
        response = self.client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/groups/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/groups/10/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/api/groups/', {
            "title": "test",
            "section": 1
        })
        self.assertEqual(response.status_code, 403)

        response = self.client.put('/api/groups/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/groups/1/', {})
        self.assertEqual(response.status_code, 403)

    def test_sections_api(self):
        response = self.client.get('/api/sections/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/sections/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/sections/10/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/api/sections/', {
            "title": "test"
        })
        self.assertEqual(response.status_code, 403)

        response = self.client.put('/api/sections/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/sections/1/', {})
        self.assertEqual(response.status_code, 403)

    def test_items_api(self):
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/items/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/items/10/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/api/items/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.put('/api/items/1/', {})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete('/api/items/1/', {})
        self.assertEqual(response.status_code, 403)

