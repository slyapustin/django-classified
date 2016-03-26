# -*- coding:utf-8 -*-

from django.contrib import admin

from dcf.models import Section, Group, Item, Image


class ImageInline(admin.StackedInline):
    model = Image
    extra = 5


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'slug', 'user', 'is_active', 'posted', 'updated', 'group')
    list_filter = ('group', 'is_active', 'posted', )
    search_fields = ('title', 'body', 'user__email')
    inlines = [ImageInline]


class GroupAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'slug', 'section', 'count')
    list_filter = ('section',)
    search_fields = ('title', 'section__title')


class SectionAdmin(admin.ModelAdmin):

    list_display = ('title',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('phone')


admin.site.register(Section, SectionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Item, ItemAdmin)
