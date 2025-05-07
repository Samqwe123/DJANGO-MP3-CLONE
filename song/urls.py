
from . import views
from django.contrib import admin
from django.urls import path , include


urlpatterns = [
    path('' , views.index , name = 'index' ),
    path('register' , views.register_user , name='register'),
    path('login' , views.login_user , name='login' ),
    path('logout' , views.logout_user , name='logout'),
    path('add_playlist/' , views.create_playlist , name = "add_playlist"),
    path('view_playlist/<int:pk>/' , views.view_playlist , name = "view_playlist"),
    path('all_playlist', views.all_playlist , name = "all_playlists"),
]
