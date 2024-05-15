from . import views
from django.urls import path


urlpatterns = [
   
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag, name='tag'),
    path('bookmark/<slug:slug>', views.bookmark, name='bookmark'),
    path('likes/<slug:slug>', views.post_likes, name='likes'),
    path('bookmarked_posts', views.bookmarked_posts, name='bookmarked_posts'),
    path('all_posts', views.all_posts, name='all_posts'),
    path('all_likes', views.all_likes, name='all_likes')
]
