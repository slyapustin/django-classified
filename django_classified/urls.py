from django.urls import re_path
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.views.decorators.cache import cache_page, never_cache

from . import views, feeds, sitemap

app_name = 'django_classified'

urlpatterns = [
    re_path(r'^$', views.SectionListView.as_view(), name='index'),
    re_path(r'^new/$', never_cache(views.ItemCreateView.as_view()), name='item-new'),
    re_path(r'^edit/(?P<pk>\d+)/$', never_cache(views.ItemUpdateView.as_view()), name='item-edit'),
    re_path(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.ItemDetailView.as_view(), name='item'),
    re_path(r'^group/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.GroupDetail.as_view(), name='group'),
    re_path(r'^search/', views.SearchView.as_view(), name='search'),
    re_path(r'^robots\.txt$', cache_page(60 * 60)(views.RobotsView.as_view()), name='robots'),
    re_path(r'^sitemap\.xml$', sitemap_view, {'sitemaps': sitemap.sitemaps_dict}, name='sitemap'),
    re_path(r'^rss\.xml$', cache_page(60 * 15)(feeds.LatestItemFeed()), name='rss'),
    re_path(r'^user/$', views.MyItemsView.as_view(), name='user-items'),
    re_path(r'^user/profile/$', views.ProfileView.as_view(), name='profile'),
    re_path(r'^user/my/delete/(?P<pk>\d+)/$', views.ItemDeleteView.as_view(), name='my-delete'),
    re_path(r'^user/logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^user/set-area/$', views.SetAreaView.as_view(), name='set-area'),
]
