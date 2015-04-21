# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.decorators.cache import cache_page

from dcf import views, feeds, sitemap

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', cache_page(60 * 15)(views.index)),

    url(r'^new$', views.ItemCreateView.as_view(), name='item-new'),
    url(r'^edit/(?P<pk>\d+)$', views.ItemUpdateView.as_view(), name='item-edit'),

    # listings
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)$', cache_page(60 * 15)(views.ItemDetailView.as_view()), name='item'),
    url(r'^group/(?P<pk>\d+)-(?P<slug>[-\w]+)$', cache_page(60 * 15)(views.GroupDetail.as_view()), name='group'),

    url(r'^search/', views.SearchView.as_view(), name='search'),
    url(r'^robots\.txt$', views.robots),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap.sitemaps_dict}),
    url(r'^rss\.xml$', cache_page(60 * 15)(feeds.LatestItemFeed()), name='rss'),

    url(r'^user/$', views.MyItemsView.as_view(), name='my'),
    url(r'^user/profile/$', views.view_profile, name='profile'),
    url(r'^user/my/delete/(?P<pk>\d+)$', views.ItemDeleteView.as_view(), name='my-delete'),

    # authorization
    url(r'user/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^user/login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^admin/', include(admin.site.urls)),

)

handler404 = views.page404
handler403 = views.page403
handler500 = views.page500

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)