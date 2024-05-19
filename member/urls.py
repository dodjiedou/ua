from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
      get_member_profile,login,
      create_alerte,get_member_alerte,
      get_members,get_categorie,
      create_message,update_member_photo_profile,
      get_forum_message
    )


urlpatterns = [

    # Api
    path('api-login/', login, name="api-login" ),
    path('member-profile/',get_member_profile, name='member-profile'),
    path('update-member-photo-profile/',update_member_photo_profile, name='update-member-photo-profile'),
    path('create-alerte/',create_alerte, name='create-alerte'),
    path('member-alerte/',get_member_alerte, name='member-alerte'),
    path('members/',get_members, name='members'),
    path('categorie/',get_categorie, name='categorie'),
    path('create-message/',create_message, name='create_message'),
    path('get-forum-message/',get_forum_message, name='get-forum-message'),

]
 
