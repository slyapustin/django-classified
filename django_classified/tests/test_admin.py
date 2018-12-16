from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AdminTestCase(TestCase):
    """Django Admin Panel Test Case"""

    def setUp(self):
        username = 'test_admin'
        pwd = 'secret'

        self.admin = User.objects.create_user(
            username,
            '',
            pwd,
            is_staff=True,
            is_superuser=True,
        )
        self.admin.save()
        self.assertTrue(self.client.login(username=username, password=pwd))

    def tearDown(self):
        self.client.logout()
        self.admin.delete()


class ItemsAdminTestCase(AdminTestCase):
    def test_(self):
        response = self.client.get(
            reverse('admin:django_classified_item_changelist'),
            {'q': 'test'},
        )

        self.assertEqual(response.status_code, 200)
