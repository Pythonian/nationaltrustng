from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category, name='category'),    
    path('post/<slug:slug>/', views.post, name='post'),
    path('', views.home, name='home'),
]