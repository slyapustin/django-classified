from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'', include('django_classified.urls', namespace='django_classified')),
    url(r'^admin/', admin.site.urls),
]
