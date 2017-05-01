# -*- coding:utf-8 -*-
from StringIO import StringIO

from django.core.management import call_command
from django.test import TransactionTestCase


class TestCommandsCase(TransactionTestCase):

    def test_execute_command(self):
        out = StringIO()
        call_command('notification_manager', stdout=out)
        self.assertIn('', out.getvalue())

