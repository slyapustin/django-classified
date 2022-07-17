from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('', include('django_classified.urls', namespace='django_classified')),
    path('admin/', admin.site.urls),
]
