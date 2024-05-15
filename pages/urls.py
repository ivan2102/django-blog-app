from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('author/<slug:slug>', views.author, name='author'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about')
]
