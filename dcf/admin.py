# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

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


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'last_login', 'date_joined', 'is_active', 'receive_news')
    list_filter = ('last_login', 'date_joined', 'is_active')
    search_fields = ('username', 'email')


admin.site.register(Section, SectionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Item, ItemAdmin)

admin.site.register(get_user_model(), CustomUserAdmin)
