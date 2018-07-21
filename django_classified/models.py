# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from sorl.thumbnail import ImageField
from unidecode import unidecode

from . import settings as dcf_settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(_('Contact phone'), max_length=30, null=True, blank=True)
    receive_news = models.BooleanField(_('receive news'), default=True, db_index=True)

    def allow_add_item(self):
        return self.user.item_set.count() < dcf_settings.ITEM_PER_USER_LIMIT

    @staticmethod
    def get_or_create_for_user(user):
        if hasattr(user, 'profile'):
            return user.profile
        else:
            return Profile.objects.create(user=user)


@python_2_unicode_compatible
class Area(models.Model):
    slug = models.SlugField()
    title = models.CharField(_('title'), max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    @classmethod
    def get_for_request(cls, request):
        if 'area_pk' in request.session:
            try:
                return cls.objects.get(pk=request.session['area_pk'])
            except cls.DoesNotExist:
                return None
        return None

    def set_for_request(self, request):
        request.session['area_pk'] = self.pk

    @classmethod
    def delete_for_request(cls, request):
        if 'area_pk' in request.session:
            del request.session['area_pk']


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
    section = models.ForeignKey('Section', verbose_name=_('section'), on_delete=models.CASCADE)

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
        return reverse('django_classified:group', kwargs={'pk': self.pk, 'slug': self.slug})


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


@python_2_unicode_compatible
class Item(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name=_('group'), on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name=_('area'), on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(_('active'), default=True, db_index=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, db_index=True)
    posted = models.DateTimeField(_('posted'), auto_now_add=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        if not self.is_active:
            return '[%s] %s' % (_('in active'), self.title)
        else:
            return self.title

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('-updated', )

    def get_absolute_url(self):
        return reverse('django_classified:item', kwargs={
            'pk': self.pk,
            'slug': self.slug
        })

    @cached_property
    def get_keywords(self):
        return ",".join(set(self.description.split()))

    @cached_property
    def contact_phone(self):
        return self.user.profile.phone

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

        return qs[:dcf_settings.RELATED_LIMIT]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Item, self).save(*args, **kwargs)


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    file = ImageField(_('image'), upload_to='images')
