from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
import cloudinary
import datetime as dt

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(null=True)
    profile_photo = CloudinaryField('profile_photo', null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Tutorial(models.Model):
    title = models.CharField(max_length = 60)
    description = models.TextField()
    tutorial_image = CloudinaryField('tutorial_image', null=True)
    tutorial_content = models.TextField()
    tutorial_author = models.CharField(max_length = 30)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    published = models.BooleanField(default=False)
    prof_ref = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tutorials', null=True)

    class Meta:
    
        ordering = ['created_on']

    @classmethod
    def search_project(cls, search_term):
        tuts = cls.objects.filter(title__icontains=search_term)
        return tuts

    
    def __str__(self):
        return self.title