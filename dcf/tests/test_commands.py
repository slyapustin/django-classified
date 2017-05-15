# -*- coding:utf-8 -*-

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core import management
from django.test import TestCase
from django.core import mail

from dcf.models import Item, Group, Section
from StringIO import StringIO


class GenericViewTestCase(TestCase):

    def setUp(self):

        management.call_command('loaddata', 'dcf/tests/init_data_for_command_test.json', verbosity=0)


class TestCommands(GenericViewTestCase):

    def test_alert(self):

        mail.outbox=[]

        out = StringIO()
        management.call_command('alert_before_remove_item')
        self.assertEqual(len(mail.outbox), 3)
        self.assertEquals(out.getvalue(), '')

    def test_remove(self):

        out = StringIO()
        management.call_command('remove_old_items')
        self.assertEquals(out.getvalue(), '')
        items = Item.objects.filter(is_active=0).count()
        self.assertEqual(items, 4)
