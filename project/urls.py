# -*- coding:utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout, login

admin.autodiscover()

urlpatterns = [
    # Authorization
    url(r'^user/', include('social_django.urls', namespace='social')),
    url(r'^user/login/', login, name='login'),
    url(r'^user/logout/$', logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('dcf.urls', namespace='dcf')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
