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
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('privacy/', views.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('advertise/', views.flatpage, {'url': '/advertise/'}, name='advertise'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('news.urls', namespace='news')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'National Trust CMS'
admin.site.index_title = 'Admin Dashboard'
admin.site.site_title = 'National Trust Administration'

handler500 = 'news.views.error_500'
handler404 = 'news.views.error_404'
