from django.urls import path
from .feeds import LatestPostsFeed
from . import views

app_name = 'news'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('archive/', views.archive, name='archive'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('category/<slug:slug>/', views.category, name='category'),    
    path('post/<slug:slug>/', views.post, name='post'),
    path('', views.home, name='home'),
]