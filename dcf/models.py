# -*- coding:utf-8 -*-
from sorl.thumbnail import ImageField
from unidecode import unidecode

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(_('phone'), max_length=30, null=True, blank=True)
    receive_news = models.BooleanField(_('receive news'), default=True, db_index=True)

    def allow_add_item(self):
        if self.item_set.count() > settings.DCF_ITEM_PER_USER_LIMIT:
            return False
        else:
            return True


class Section(models.Model):
    title = models.CharField(_('title'), max_length=100)

    def __unicode__(self):
        return self.title

    def count(self):
        return Item.objects.filter(is_active=True)\
            .filter(group__section=self).count()


class Group(models.Model):
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(_('title'), max_length=100)
    section = models.ForeignKey('Section')

    def __unicode__(self):
        return u'%s - %s' % (self.section.title, self.title)

    def count(self):
        return self.item_set.filter(is_active=True).count()

    class Meta:
        ordering = ['section__title', 'title', ]

    def get_title(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(unidecode(self.title))
        super(Group, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('group', kwargs={'pk': self.pk, 'slug': self.slug})


class Item(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    group = models.ForeignKey(Group, verbose_name="group")

    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    phone = models.CharField(_('phone'), max_length=30)
    is_active = models.BooleanField(_('display'), default=True, db_index=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, db_index=True)
    posted = models.DateTimeField(_('posted'), auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-updated', )

    def get_absolute_url(self):
        return reverse('item', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_title(self):
        return u'%s' % self.title

    def get_description(self):

        return u'%s' % self.description[:155]

    def get_keywords(self):

        # TODO need more optimal keywords selection
        return ",".join(set(self.description.split()))

    def get_related(self):

        # TODO Need more complicated related select
        return Item.objects.exclude(pk=self.pk)[:settings.DCF_RELATED_LIMIT]

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(unidecode(self.title))
        super(Item, self).save(*args, **kwargs)


class Image(models.Model):
    item = models.ForeignKey(Item)
    file = ImageField(_('image'), upload_to='images')
