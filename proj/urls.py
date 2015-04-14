from django.conf.urls import patterns, include, url
from django.contrib import admin

from dcf import views, feeds, sitemap

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.index),

    url(r'^user/my/delete/(?P<pk>\d+)\.html$', views.delete, name='my-delete'),

    url(r'^new$', views.ItemCreateView.as_view(), name='item-new'),
    url(r'^edit/(?P<pk>\d+)$', views.ItemUpdateView.as_view(), name='item-edit'),

    # listings
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)$', views.ItemDetailView.as_view(), name='item'),
    url(r'^group/(?P<pk>\d+)-(?P<slug>[-\w]+)$', views.GroupDetailView.as_view(), name='group'),

    url(r'^search/', views.SearchView.as_view(), name='search'),
    url(r'^robots\.txt$', views.robots),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap.sitemaps_dict}),
    url(r'^rss\.xml$', feeds.LatestItemFeed(), name='rss'),

    url(r'^user/$', views.MyItemsView.as_view(), name='my'),
    url(r'^user/profile/$', views.view_profile, name='profile'),

    url(r'^user/login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^admin/', include(admin.site.urls)),
)