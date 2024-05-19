from rest_framework import serializers
from .models import Message
from users.models import Member, Alerte
from focalpoint.models import FocalPoint,Categorie
import base64



class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MemberProfileSerializer(serializers.ModelSerializer):
    member_photo = serializers.SerializerMethodField(method_name="get_member_photo")
    #country = serializers.SerializerMethodField(method_name="get_country_name")
    ##focal_point = serializers.SerializerMethodField(method_name="get_focal_point_name")
    class Meta:
        model = Member
        fields = [
            'nom',
            'prenom',
            'email',
            'city',
            'date_of_birth',
            'phone',
            'member_photo',       
        ]

    def get_member_photo(self, obj):
        member=Member.objects.get(id=obj.id)
        
        with open(member.photo, 'rb') as image_file:
            image_data = image_file.read()
    
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        data={

            'photo': base64_image,

        }
        return data

    # def get_country_name(self, obj):
    #     return obj.country.name
    
    # def get_focal_point_name(self, obj):
    #     fp=FocalPoint.objects.get(id=obj.focal_point_id)
    #     return fp.name


class MemberPhotoProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'photo',       
        ]


class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = '__all__'


class GetCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'
        


class GetAlerteSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField(method_name="get_member")
    class Meta:
        model = Alerte
        fields = [
            'member',
            'categorie',
            'contenu',
            'file',
            'date_creation',
        ]

    def get_member(self, obj):
        member=Member.objects.get(id=obj.membre_id)
        data={
            'first_name': member.prenom,
            'last_name':member.nom,
            'email':member.email,
            'city': member.city,
            'date_of_birth':member.date_of_birth
        }
        return data
    

class GetMessageSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField(method_name="get_member")
    class Meta:
        model = Message
        fields = [
            'message','media','member','created_at',
        ]

    def get_member(self, obj):
        member=Member.objects.get(id=obj.member_id)
        data={
            'first_name': member.prenom,
            'last_name':member.nom,
            'email':member.email,
            'city': member.city,
            'date_of_birth':member.date_of_birth
        }
        return data


class SetMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'message','media','member','forum',
        ]

    



