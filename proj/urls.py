# -*- coding:utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout, login
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache
from django.conf.urls.static import static

from dcf import views, feeds, sitemap
from dcf.api.routers import router

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.SectionListView.as_view()),

    url(r'^new/$', never_cache(views.ItemCreateView.as_view()), name='item-new'),
    url(r'^edit/(?P<pk>\d+)/$', never_cache(views.ItemUpdateView.as_view()), name='item-edit'),

    # Listings
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.ItemDetailView.as_view(), name='item'),
    url(r'^group/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.GroupDetail.as_view(), name='group'),

    url(r'^search/', views.SearchView.as_view(), name='search'),
    url(r'^robots\.txt$', cache_page(60 * 60)(views.RobotsView.as_view()), name='robots'),

    url(r'^sitemap\.xml$', sitemap_view, {'sitemaps': sitemap.sitemaps_dict}, name='sitemap'),
    url(r'^rss\.xml$', cache_page(60 * 15)(feeds.LatestItemFeed()), name='rss'),

    url(r'^user/$', views.MyItemsView.as_view(), name='my'),
    url(r'^user/profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^user/my/delete/(?P<pk>\d+)/$', views.ItemDeleteView.as_view(), name='my-delete'),

    # Authorization
    url(r'user/', include('social_django.urls', namespace='social')),
    url(r'^user/login/', login, name='login'),
    url(r'^user/logout/$', logout, name='logout'),

    # API
    url(r'^api/', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),
]

handler404 = views.page404
handler403 = views.page403
handler500 = views.page500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)