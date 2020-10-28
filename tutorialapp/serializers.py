from rest_framework import serializers 
from .models import Profile, Tutorial

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
 
class TutorialSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'tutorial_image',
                  'tutorial_content',
                  'created_on',
                  'updated_on',
                  'published',)