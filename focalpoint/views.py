from collections import UserList
from multiprocessing import AuthenticationError
from tkinter.ttk import Entry
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
from django.http import JsonResponse

from member.models import Member
from member.serializers import MemberSerializer
from .models import FocalPoint, Information, Publication
from .serializers import (
    FocalPointSerializer, 
    InformationSerializer,
    MediaSerializer
)


def index(request):
    focalpoints = FocalPoint.objects.all()
    nombreFocalPoint=len(focalpoints)
    utilisateurs=len(Member.objects.all())
    return render(
        request, 
        'focalpoint/admin/index.html',
        {
            'focalpoints': focalpoints,
            'nombreFocalPoint' : nombreFocalPoint,
            'utilisateurs': utilisateurs  
        }
    )


def listePointFocal(request):
    focalpoints = FocalPoint.objects.all()
    return render(
        request, 
        'focalpoint/admin/focalpoint/liste.html',
        {
            'focalpoints': focalpoints,
        }
    )


#-----------------------------API FUNCTIONS-----------------------
'''ceci recupere toutes les informations pour un point focal'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_informations(request):
    member = Member.objects.get(user_ptr_id=request.user.id)
    focal_point= member.focal_point
    publications= Publication.objects.filter(publicationfocalpoint__is_active=True)
    
    informations=[]
    for publication in publications:
        informations.append(publication.information)

    serializer = InformationSerializer(informations,many=True)
    return Response(serializer.data)

    
engine = create_engine('sqlite:///sqlite3.db')
Session = sessionmaker(bind=engine)
session = Session()
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def recherchenformation(lettres):
    informations = session.query(Information).filter(ImportError.nom.startswith(lettres)).all()
    return Response(InformationSerializer(informations))  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def research_information():
    recherche = Entry.get()
    conn = sqlite3.connect('sqlite3.db')
    cursor = conn.cursor()
    informations=cursor.execute("SELECT * FROM information WHERE title LIKE ?", ('%' + recherche + '%',))
    resultats = cursor.fetchall()
    conn.close()
    serializer = InformationSerializer(informations,many=True)
    return Response(serializer.data)

 
    

