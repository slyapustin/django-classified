from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.views.decorators.cache import cache_page, never_cache

from . import views, feeds, sitemap

app_name = 'django_classified'

urlpatterns = [
    path('', views.SectionListView.as_view(), name='index'),
    path('new/', never_cache(views.ItemCreateView.as_view()), name='item-new'),
    path('edit/<int:pk>/', never_cache(views.ItemUpdateView.as_view()), name='item-edit'),
    re_path(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.ItemDetailView.as_view(), name='item'),
    re_path(r'^group/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.GroupDetail.as_view(), name='group'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('robots.txt', cache_page(60 * 60)(views.RobotsView.as_view()), name='robots'),
    path('sitemap.xml', sitemap_view, {'sitemaps': sitemap.sitemaps_dict}, name='sitemap'),
    path('rss.xml', cache_page(60 * 15)(feeds.LatestItemFeed()), name='rss'),
    path('user/', views.MyItemsView.as_view(), name='user-items'),
    path('user/profile/', views.ProfileView.as_view(), name='profile'),
    path('user/my/delete/<int:pk>/', views.ItemDeleteView.as_view(), name='my-delete'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('user/set-area/', views.SetAreaView.as_view(), name='set-area'),
]
