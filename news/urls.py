from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('post/', views.post, name='post'),
    path('', views.home, name='home'),
]