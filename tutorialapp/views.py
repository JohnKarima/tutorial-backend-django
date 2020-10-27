from django.shortcuts import render, redirect
from django.contrib import messages
from django.http  import HttpResponse
from .models import Profile, User, Tutorial
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TutorialUploadForm
from django.contrib.auth.decorators import login_required
from cloudinary.forms import cl_init_js_callbacks
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from rest_framework import generics
from .serializers import ProfileSerializer, TutorialSerializer
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
@login_required
def index(request):
    tutorials = Tutorial.objects.all()
    users = User.objects.all()
    return render(request, 'index.html', {"tutorials":tutorials[::-1], "users": users})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Successfully created account created for {username}! Please log in to continue')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    tutorials = request.user.profile.tutorials.all()
    return render(request, 'users/profile.html', {"tutorials":tutorials[::-1]})

class ListProfileView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

@login_required
def update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
        instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Successfully updated your account!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/update.html', context)

@login_required
def upload_tutorial(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == "POST":
        form = TutorialUploadForm(request.POST, request.FILES)
        if form.is_valid():
            tutorial = form.save(commit = False)
            tutorial.prof_ref = request.user.profile
            tutorial.save()
            messages.success(request, f'Successfully uploaded your Tutorial!')
            return redirect('index')
    else:
        form = TutorialUploadForm()
    return render(request, 'upload_tutorial.html', {"form": form, "users": users})

def tutorial(request,tutorial_id):
    try:
        tutorial = Tutorial.objects.get(id = tutorial_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"tutorial.html", {"tutorial":tutorial})

class ListTutorialView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

@login_required
def search_results(request):
    if 'tutorial' in request.GET and request.GET["tutorial"]:
        search_term = request.GET.get("tutorial")
        searched_tutorials = Tutorial.search_tutorial(search_term)
        message = f"{search_term}"
        return render(request, 'search.html', {"message":message,"tutorials": searched_tutorials})
    else:
        message = "You haven't searched for any tutorials yet"
    return render(request, 'search.html', {'message': message})