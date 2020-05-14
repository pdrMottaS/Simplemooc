"""simplemooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from simplemooc.core import core_urls
from simplemooc.courses import courses_urls
from simplemooc.accounts import accounts_urls
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as views_auth

urlpatterns = [
    path('', include((core_urls, 'core'), namespace='core')),
    path('user/', include((accounts_urls, 'accounts'), namespace='accounts')),
    path('courses/', include((courses_urls, 'courses'), namespace='courses')),
    path('admin/', admin.site.urls),
    path('reset_password/', views_auth.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', views_auth.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views_auth.PasswordResetConfirmView.as_view(template_name='registration/password_reset_fields.html'), name='password_reset_confirm'),
    path('reset_password_complete/', views_auth.PasswordResetCompleteView.as_view(template_name="registration/password_reset_end.html"), name='password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
