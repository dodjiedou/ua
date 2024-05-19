from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser

from focalpoint.models import Forum
from users.models import Member


class MemberProfile(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE, default=1)
    focal_point = models.IntegerField()


class Notification(models.Model):
    message = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField(null=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    #media = models.FileField(null=True,blank=True, upload_to='focalpoint/forum')
    media = models.TextField(null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

