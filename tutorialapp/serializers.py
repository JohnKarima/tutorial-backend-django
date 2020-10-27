from rest_framework import serializers 
from .models import Profile, Tutorial

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("user", "bio", "profile_photo")
 
class TutorialSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'tutorial_image',
                  'tutorial_content',
                  'created_on',
                  'published',)