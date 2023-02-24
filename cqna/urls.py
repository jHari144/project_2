from django.urls import path

from . import views

app_name = 'cqna'

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('home', views.user_posts, name='user_posts'),
    path('create_post', views.create_post, name='create_post'),
    path('create_post/add_tags', views.add_tags, name='add_tags'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('<int:post_id>/edit_post/', views.edit_post, name='edit_post'),
    path('<int:post_id>/edit_tags/', views.edit_tags, name='edit_tags'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/reply/', views.reply, name='reply'),
    path('search_tag/', views.search_tag, name='search_tag'),
    path('search_user/', views.search_user, name='search_user'),
    path('search/', views.call_search, name='search'),
]
