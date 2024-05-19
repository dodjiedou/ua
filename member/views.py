import binascii
from django.conf import settings
from rest_framework.authtoken.models import Token
import os
import random
import secrets
import string
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import generics, permissions
from rest_framework.decorators import authentication_classes, permission_classes
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from io import BytesIO
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from focalpoint.models import FocalPoint
from onesignal_sdk.client import Client
import requests

from focalpoint.models import Information,Forum,Categorie
from .models import Notification,Message
from users.models import Member,Commentaire, Like, Alerte
from .serializers import (
    MemberSerializer,
    MemberProfileSerializer, 
    MemberPhotoProfileSerializer,
    GetAlerteSerializer,
    GetCategorieSerializer,
    GetMessageSerializer,SetMessageSerializer,
    AlerteSerializer)

#-----------------------------API FUNCTIONS-----------------------
'''ceci est api de connexion,la connexion se fait avec l'email
et le mot de passe
url :  path('api-login/', login, name="api-login" ),
''' 
@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    try:

        if Member.objects.filter(email=email).exists():

            member = Member.objects.get(email=email)

            if member.is_active==0:
                data = {
                    "status": 0,
                    "message": "Votre Compte est désactivé. veuillez contacter le support"
                }
                return Response(data)
            else:

                if authenticate(request, email=email, password=password):

                    if Token.objects.filter(user_id=member.id).exists():

                        key = binascii.hexlify(os.urandom(20)).decode()
                        Token.objects.filter(user_id=member.id).update(key=key)
                        token = Token.objects.get(user_id=member.id)

                        #update_last_login(None, member)

                    else:

                        key = binascii.hexlify(os.urandom(20)).decode()
                        Token.objects.create(user_id=member.id, key=key)
                        token = Token.objects.get(user_id=member.id)

                    data = {
                        'status': 1,
                        'token': str(token.key),
                        'message': "Vous êtes connecté avec succès"
                    }
                    return Response(data)

                else:

                    data = {
                        "status": 0,
                        "message": "Erreur de connexion! Vos informations fournies sont incorrectes."
                    }

                    return Response(data)

        else:

            data = {
                "status": 0,
                "message": "Nous n'avons pas trouvé un compte lié avec ces informations"
            }

            return Response(data)

    except KeyError as e:

        return Response({"da": 'I got a KeyError - reason "%s"' % str(e)})

'''ceci renvoie les informations sur un membre, les informations 
a afficher sur son profil'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_member_profile(request):
    member = Member.objects.get(user_ptr_id=request.user.id)
    serializer = MemberProfileSerializer(member)
    return Response(serializer.data)


'''afficher la photo de profile du membre'''
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_member_phto_profile(request):
#     member = Member.objects.get(user_ptr_id=request.user.id)
#     serializer = MemberProfileSerializer(member)
#     return Response(serializer.data)


'''ceci permet la modification des informations du profil du membre'''
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_member_photo_profile(request):
    member=Member.objects.get(user_ptr_id=request.user.id)
    longueur_chaine = 10
    random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(longueur_chaine))
    
    if "photo" in request.data:
        profile_picture=request.data["photo"]
    else:
        profile_picture=None
 
    if "base64" in profile_picture:
        format,imgstr = profile_picture.split(';base64,')
        photo = imgstr
        file_extension = format.split('/')[-1]
    else:
        file_extension = "jpeg"
        photo = profile_picture
    
    file_name = "profile_" + str(member.prenom) + '_' + str(random_name) + "." + str(file_extension)
    full_path = os.path.join(settings.MEDIA_ROOT, file_name)
    with open(full_path, "wb") as fh:
        fh.write(base64.b64decode(photo.encode('utf-8')))
        chemin_relatif=os.path.relpath(file_name, settings.MEDIA_ROOT )
       
    serializer = MemberPhotoProfileSerializer(member,
        data={
            # 'photo': chemin_relatif,
            'photo': "media/"+file_name,
        }
    )

    if serializer.is_valid():
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''ceci retourne la liste de tous les membres dun point focal'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_members(request):
    member = Member.objects.get(user_ptr_id=request.user.id)
    members = Member.objects.filter(focal_point_id=member.focal_point_id)
    serializer = MemberProfileSerializer(members,many=True)
    return Response(serializer.data)

'''cette api était créée pour retournér toutes les categories
d alerte mais on ne l a plus utiliser'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categorie(request):
    categories = Categorie.objects.all()
    serializer = GetCategorieSerializer(categories,many=True)
    return Response(serializer.data)

'''ceci renvoie toutes les alertes qu un membre a publié'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_member_alerte(request):
    member = Member.objects.get(user_ptr_id=request.user.id)
    alertes=member.alerte_set.all()
    serializer = AlerteSerializer(alertes,many=True)
    return Response(serializer.data)
     
'''cette api permat de creer des alertes. On envoie en parametre
l alerte (le champ description) et le type(le champ alertType)'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_alerte(request):
    serializer = AlerteSerializer(
        data={
            "membre" : request.user.id,
            "contenu" : request.data["description"],
            "categorie" : request.data["alertType"],
        }
    )
    if serializer.is_valid():
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''ceci permet d envoyer des messages dans les forums depuis l application
mobile. Les champs a remplir au niveau de l application mobile
sont : media, content, '''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request):
    longueur_chaine = 10
    random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(longueur_chaine))
    member=Member.objects.get(user_ptr_id=request.user.id)
    forum=Forum.objects.get(focal_point_id=member.focal_point_id)
    
    if "media" in request.data:
        profile_picture=request.data["media"]
    else:
        profile_picture=None

    if "content" in request.data:
        message=request.data["content"]
    else:
        message=None

 
    if "base64" in profile_picture:

        format, imgstr = profile_picture.split(';base64,')
        photo = imgstr
        file_extension = format.split('/')[-1]
        content_type = "image/" + file_extension

    else:

        file_extension = "jpeg"
        content_type = "image/" + file_extension
        photo = profile_picture

    file_name = "profile_" + str(member.prenom) + '_' + str(random_name) + "." + str(file_extension)
    
    full_path = os.path.join(settings.MEDIA_ROOT, file_name)

    with open(full_path, "wb") as fh:
    # with open(str(file_name), "wb") as fh:
        fh.write(base64.b64decode(photo.encode('utf-8')))
        #chemin_absolu=os.path.abspath(file_name)
        #chemin_relatif=os.path.relpath(chemin_absolu, settings.MEDIA_URL)
        chemin_relatif=os.path.relpath(file_name, settings.MEDIA_ROOT )
    serializer = SetMessageSerializer(
        data={
            "member" : member.id,
            "message" : message,
            "media" :chemin_relatif,
            "forum" : forum.id,
        }
    )
    if serializer.is_valid():
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''ceci permet de recuperer tous les messages d'un forum'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forum_message(request):
    member=Member.objects.get(user_ptr_id=request.user.id)
    forum=Forum.objects.get(focal_point_id=member.focal_point_id)
    messages = Message.objects.filter(forum_id=forum.id)
    serializer = GetMessageSerializer(messages,many=True)
    return Response(serializer.data)
