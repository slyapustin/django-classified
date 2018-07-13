from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    url('', include('django_classified.urls', namespace='django_classified')),
    url('social/', include('social_django.urls', namespace='social')),
    url('admin/', admin.site.urls),

    # Create custom login page using default 'registration/login.html' template path
    url('login/', auth_views.LoginView.as_view(template_name='demo/login.html'), name='login'),
    url('email-sent/', TemplateView.as_view(template_name='demo/email_sent.html'))
]
