# -*- coding:utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from sorl.thumbnail import ImageField
from unidecode import unidecode

from dcf import settings as dcf_settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    phone = models.CharField(_('phone'), max_length=30, null=True, blank=True)
    receive_news = models.BooleanField(_('receive news'), default=True, db_index=True)

    def allow_add_item(self):
        return self.user.item_set.count() < dcf_settings.DCF_ITEM_PER_USER_LIMIT

    @staticmethod
    def get_or_create_for_user(user):
        if hasattr(user, 'profile'):
            return user.profile
        else:
            return Profile.objects.create(user=user)


@python_2_unicode_compatible
class Section(models.Model):
    title = models.CharField(_('title'), max_length=100)

    def __str__(self):
        return self.title

    @cached_property
    def count(self):
        return Item.objects \
            .filter(is_active=True) \
            .filter(group__section=self) \
            .count()

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


@python_2_unicode_compatible
class Group(models.Model):
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(_('title'), max_length=100)
    section = models.ForeignKey('Section', verbose_name=_('section'))

    def __str__(self):
        return '%s - %s' % (self.section.title, self.title)

    @cached_property
    def count(self):
        return self.item_set.filter(is_active=True).count()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        ordering = ['section__title', 'title', ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Group, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dcf:group', kwargs={'pk': self.pk, 'slug': self.slug})


@python_2_unicode_compatible
class Item(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    group = models.ForeignKey(Group, verbose_name=_('group'))

    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(_('display'), default=True, db_index=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, db_index=True)
    posted = models.DateTimeField(_('posted'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('-updated', )

    def get_absolute_url(self):
        return reverse('dcf:item', kwargs={
            'pk': self.pk,
            'slug': self.slug
        })

    def get_keywords(self):
        # TODO need more optimal keywords selection
        return ",".join(set(self.description.split()))

    @cached_property
    def image_count(self):
        return self.image_set.count()

    @cached_property
    def featured_image(self):
        return self.image_set.all().first()

    @cached_property
    def related_items(self):
        qs = Item.objects \
            .filter(is_active=True) \
            .filter(group=self.group) \
            .exclude(pk=self.pk)

        return qs[:dcf_settings.DCF_RELATED_LIMIT]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Item, self).save(*args, **kwargs)


class Image(models.Model):
    item = models.ForeignKey(Item)
    file = ImageField(_('image'), upload_to='images')
