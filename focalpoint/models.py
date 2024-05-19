from django.db import models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
# from .models import FocalpointPublication

# Create your models here.


class FocalPoint(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    active=models.BooleanField(default=True)
    country = CountryField(null=True, blank=True)
    access_code = models.CharField(null=True,max_length=55)
    access_pass = models.CharField(null=True,max_length=255)
    email = models.EmailField(unique=True)
    telephone=models.CharField(null=True, max_length=255)
    
    def get_country_display_full(self):
        return self.get_country_display()
    
    #cette methode retourne  le nombre de membre pour un point focal
    def nombreDeMembre(self):
        return self.member_set.count()
    
    def clean(self):
        # Validation personnalisée de l'adresse email
        if FocalPoint.objects.exclude(pk=self.pk).filter(email=self.email).exists():
            raise ValidationError('Cette adresse email est déjà utilisée par un autre point focal.')

    class Meta:
        verbose_name = 'Point Focal'
        verbose_name_plural = 'Points Focaux'

    def __str__(self):
        return self.name


class Categorie(models.Model):
    label = models.CharField(max_length=255)
    def __str__(self):
        return self.label  

class Information(models.Model):
    title = models.CharField(max_length=255)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='informations')
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    file = models.FileField(null=True,blank=True, upload_to='focalpoint/information')

    def __str__(self):
        return self.title
    

class Publication(models.Model):
    information = models.ForeignKey(Information, on_delete=models.CASCADE, related_name='informations')
    focalpoint = models.ManyToManyField(FocalPoint,through='PublicationFocalPoint')
    published_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.information.title
    

class PublicationFocalPoint(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    focalpoint = models.ForeignKey(FocalPoint, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('publication','focalpoint')

 
class Media(models.Model):
    information = models.ForeignKey(Information, on_delete=models.CASCADE, related_name='medias')
    file = models.FileField(upload_to='files/')
    media_url= models.CharField(null=True,max_length=100)
    media_type= models.CharField(null=True,max_length=100)
    is_publshed=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_member=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
       

class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    focal_point = models.ForeignKey(FocalPoint, on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
