"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from news.sitemaps import PostSitemap
from django.contrib.flatpages import views


sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('news.urls', namespace='news')),
]

urlpatterns += [
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('privacy/', views.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('advertise/', views.flatpage, {'url': '/advertise/'}, name='advertise'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
admin.site.site_header = 'National Trust CMS'
admin.site.index_title = 'Admin Dashboard'
admin.site.site_title = 'National Trust Administration'

handler500 = 'news.views.error_500'
handler404 = 'news.views.error_404'
