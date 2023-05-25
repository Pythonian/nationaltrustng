from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('category/<slug:slug>/', views.category, name='category'),    
    path('<slug:slug>/', views.post, name='post'),
    path('', views.home, name='home'),
]