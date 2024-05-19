from rest_framework import serializers
from .models import FocalPoint, Information, Media, Forum
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class FocalPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocalPoint
        fields = '__all__'
       
       
class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = [
            'title','description','categorie','file',
            #'is_published','published_at','updated_at'
            'created_at'

        ]
    
        

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = [
            'name','description','focal_point',
        ]
