from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import (
       get_informations,index, listePointFocal,research_information
    )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    # path('index/', index , name='index'),
    # path('liste-point-focal/', listePointFocal , name='liste-point-focal'),

    # Api
    path('api-auth/', include('rest_framework.urls')),
    path('api-informations/', get_informations, name='api-informations'),
    path('api-recherche/', research_information, name='api-recherche'),

]


