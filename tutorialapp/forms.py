from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Tutorial


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'bio']

class TutorialUploadForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ['title', 'description', 'tutorial_image', 'tutorial_content', 'tutorial_author']

    def form_valid(self, form):
        form.instance.user = self.request.profile
        return super().form_valid(form)

