# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.views.decorators.cache import cache_page, never_cache

from . import views, feeds, sitemap

app_name = 'django_classified'

urlpatterns = [
    url(r'^$', views.SectionListView.as_view(), name='index'),
    url(r'^new/$', never_cache(views.ItemCreateView.as_view()), name='item-new'),
    url(r'^edit/(?P<pk>\d+)/$', never_cache(views.ItemUpdateView.as_view()), name='item-edit'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.ItemDetailView.as_view(), name='item'),
    url(r'^group/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.GroupDetail.as_view(), name='group'),
    url(r'^search/', views.SearchView.as_view(), name='search'),
    url(r'^robots\.txt$', cache_page(60 * 60)(views.RobotsView.as_view()), name='robots'),
    url(r'^sitemap\.xml$', sitemap_view, {'sitemaps': sitemap.sitemaps_dict}, name='sitemap'),
    url(r'^rss\.xml$', cache_page(60 * 15)(feeds.LatestItemFeed()), name='rss'),
    url(r'^user/$', views.MyItemsView.as_view(), name='user-items'),
    url(r'^user/profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^user/my/delete/(?P<pk>\d+)/$', views.ItemDeleteView.as_view(), name='my-delete'),
    url(r'^user/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^user/set-area/$', views.SetAreaView.as_view(), name='set-area'),
]
