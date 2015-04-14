# -*- coding:utf-8 -*-

from django.test import TestCase
from dcf.models import Item, Group, Section
from django.contrib.auth import get_user_model


class TestUpdateView(TestCase):

    def setUp(self):

        user_class = get_user_model()
        self.user = user_class.objects.create(username="test")

    def test_item_creation(self):

        section = Section.objects.create(title='Cars')
        group = Group.objects.create(title=u'Electric Cars', section=section)

        item = Item.objects.create(user=self.user, group=group, title=u'Tesla S',
                                   description='Super new 2015 Tesla S electric Car', price=79000.00, phone='1-121-12-90')

        self.assertEquals(Item.objects.count(), 1)
        self.assertEquals(item.get_absolute_url(), '/1-tesla-s')