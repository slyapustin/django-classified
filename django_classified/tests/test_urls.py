from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django_classified.models import Item, Group, Profile, Section
from django_classified.settings import ITEM_PER_USER_LIMIT


class BaseTestCase(TestCase):
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


class DCFTestCase(BaseTestCase):
    def test_index_page(self):
        response = self.client.get(reverse('django_classified:index'))
        self.assertContains(response, self.group.section.title)

    def test_pages(self):
        response = self.client.get(reverse('django_classified:robots'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('django_classified:search'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('django_classified:sitemap'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('django_classified:rss'))
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

        response = self.client.get(reverse('django_classified:profile'))
        self.assertContains(response, self.profile.phone)

        new_data = {'phone': '1111111111'}
        self.client.post(reverse('django_classified:profile'), new_data)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, new_data['phone'])

    def test_item_search_by_title(self):
        response = self.client.get(reverse('django_classified:search'), {'q': self.item.title})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_by_description(self):
        response = self.client.get(reverse('django_classified:search'), {'q': self.item.description})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_by_group(self):
        response = self.client.get(reverse('django_classified:search'), {'group': self.item.group.pk})
        self.assertContains(response, self.item.get_absolute_url())

    def test_item_search_not_found(self):
        response = self.client.get(reverse('django_classified:search'), {'q': 'WRONG KEYWORDS'})
        self.assertNotContains(response, self.item.get_absolute_url())

    def test_item_search_by_title_only(self):
        item = Item.objects.create(
            user=self.user,
            group=self.group,
            title='Unique Gadget XYZ',
            description='A regular product listing',
            price=50,
        )
        response = self.client.get(reverse('django_classified:search'), {'q': 'Gadget XYZ'})
        self.assertContains(response, item.get_absolute_url())

    def test_item_search_multi_word_matches_across_fields(self):
        item = Item.objects.create(
            user=self.user,
            group=self.group,
            title='Vintage Camera',
            description='Excellent condition, barely used',
            price=200,
        )
        # 'Vintage' is in title, 'condition' is in description
        response = self.client.get(reverse('django_classified:search'), {'q': 'Vintage condition'})
        self.assertContains(response, item.get_absolute_url())

    def test_item_search_multi_word_partial_miss(self):
        # All words must match somewhere
        response = self.client.get(reverse('django_classified:search'), {'q': 'Tesla NONEXISTENT'})
        self.assertNotContains(response, self.item.get_absolute_url())

    def test_user_can_add_item(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        self.assertTrue(self.profile.allow_add_item(), True)

        response = self.client.get(reverse('django_classified:item-new'))
        self.assertEqual(response.status_code, 200)

        item_data = {
            'image_set-TOTAL_FORMS': 1,
            'image_set-INITIAL_FORMS': 0,
            'group': self.group.pk,
            'title': 'iPhone X',
            'description': 'New, Unlocked. Face ID',
            'price': 999,
            'is_active': True
        }
        response = self.client.post(reverse('django_classified:item-new'), item_data, follow=True)
        self.assertContains(response, item_data['title'])
        new_item = Item.objects.filter(title=item_data['title'])
        self.assertIsNotNone(new_item)

    def test_user_can_update_item(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        self.assertEqual(self.user.item_set.count(), 1)

        response = self.client.get(reverse('django_classified:item-edit', kwargs={'pk': self.item.pk}))
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
        response = self.client.post(reverse('django_classified:item-edit', kwargs={'pk': self.item.pk}), item_data,
                                    follow=True)
        self.assertEqual(self.user.item_set.count(), 1)
        self.assertContains(response, item_data['title'])
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, item_data['title'])

    def test_another_user_cannot_update_other_user_item(self):
        another_user = get_user_model().objects.create_user(
            'Andy',
            'andy@hotmail.com',
            'pass'
        )

        self.client.login(
            username=another_user.username,
            password='pass'
        )

        self.assertEqual(another_user.item_set.count(), 0)

        response = self.client.get(reverse('django_classified:item-edit', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 403)

        item_data = {
            'image_set-TOTAL_FORMS': 0,
            'image_set-INITIAL_FORMS': 0,
            'group': self.group.pk,
            'title': 'iPhone X',
            'description': 'New, Unlocked. Face ID',
            'price': 999,
            'is_active': True
        }
        response = self.client.post(reverse('django_classified:item-edit', kwargs={'pk': self.item.pk}), item_data,
                                    follow=True)
        self.assertEqual(response.status_code, 403)

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
        for i in range(self.user.item_set.count(), ITEM_PER_USER_LIMIT + 10):
            self.client.post(reverse('django_classified:item-new'), item_data)

        self.assertFalse(self.profile.allow_add_item())
        self.assertEqual(self.user.item_set.count(), ITEM_PER_USER_LIMIT)

    def test_user_can_delete_item(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        self.assertEqual(Item.objects.all().count(), 1)
        response = self.client.get(reverse('django_classified:my-delete', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)

        self.client.post(reverse('django_classified:my-delete', kwargs={'pk': self.item.pk}))
        self.assertEqual(Item.objects.all().count(), 0)

    def test_user_can_view_own_items(self):
        self.client.login(
            username=self.username,
            password=self.password
        )
        self.assertEqual(Item.objects.all().count(), 1)
        response = self.client.get(reverse('django_classified:user-items'))
        self.assertContains(response, self.item.get_absolute_url())

    def test_related_items(self):
        new_item = Item.objects.create(
            user=self.user,
            title='Tesla Model X',
            group=self.group,
            description='Old Tesla car in good shape',
            price=11000
        )

        response = self.client.get(self.item.get_absolute_url())
        self.assertContains(response, new_item.get_absolute_url())

    def test_group_slug_autocreated(self):
        section = Section.objects.first()
        new_group = Group.objects.create(
            title='Some Cool Staff',
            section=section
        )

        self.assertEqual(new_group.slug, 'some-cool-staff')

        # Test with non-Latin characters
        arabic_group = Group.objects.create(
            title='بيت للأجار',
            section=section
        )

        # The slug should preserve the Arabic characters
        self.assertEqual(arabic_group.slug, 'بيت-للأجار')

    def test_empty_section_appears_on_homepage(self):
        Section.objects.create(title='Empty Section')
        response = self.client.get(reverse('django_classified:index'))
        self.assertContains(response, 'Empty Section')

    def test_non_latin_slug_url_resolves(self):
        arabic_group = Group.objects.create(
            title='بيت للأجار',
            section=self.section
        )
        item = Item.objects.create(
            user=self.user,
            group=arabic_group,
            title='عقار جديد',
            description='A listing with Arabic title',
            price=1000,
        )
        response = self.client.get(item.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        response = self.client.get(arabic_group.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_login_required_views_redirect(self):
        protected_urls = [
            reverse('django_classified:item-new'),
            reverse('django_classified:user-items'),
            reverse('django_classified:profile'),
            reverse('django_classified:item-edit', kwargs={'pk': self.item.pk}),
            reverse('django_classified:my-delete', kwargs={'pk': self.item.pk}),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f'{url} should redirect when not logged in')

    def test_set_area_prevents_open_redirect(self):
        response = self.client.get(
            reverse('django_classified:set-area'),
            {'next': 'https://evil.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('evil.com', response.url)

    def test_set_area_allows_safe_redirect(self):
        safe_url = reverse('django_classified:search')
        response = self.client.get(
            reverse('django_classified:set-area'),
            {'next': safe_url}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, safe_url)

    def test_urls_in_description_are_clickable(self):
        item = Item.objects.create(
            user=self.user,
            group=self.group,
            title='Item with URL',
            description='Check out https://example.com for details',
            price=100,
        )
        response = self.client.get(item.get_absolute_url())
        self.assertContains(response, '<a href="https://example.com"')
