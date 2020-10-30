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
from .serializers import ProfileSerializer, TutorialSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import cloudinary.uploader
from rest_framework import viewsets
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
 
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

# class ListProfileView(generics.ListAPIView):
#     """
#     Provides a get method handler.
#     """
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

class ListProfileView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile_object = Profile.objects.all()
        profile_serialize = ProfileSerializer(profile_object, many = True)
        return Response(profile_serialize.data)
    
    def post(self, request):
        profile_serialize = ProfileSerializer(data = request.data)
        if profile_serialize.is_valid():
            profile_serialize.save()
            return Response(profile_serialize.data, status=status.HTTP_201_CREATED)
        return Response(profile_serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUpdateProfileView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.ObjectDoesNotExist:
            return Response(status.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk):
        profile_object = self.get_object(pk)
        profile_serialize = ProfileSerializer(profile_object)
        return Response(profile_serialize.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        profile_object = self.get_object(pk)
        profile_serialize = ProfileSerializer(profile_object, data=request.data)
        if profile_serialize.is_valid():
            profile_serialize.save()
            return Response(profile_serialize.data, status=status.HTTP_200_OK)
        return Response(profile_serialize.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        profile_object = self.get_object(pk)
        profile_object.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    

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

# class ListTutorialView(generics.ListAPIView):
#     """
#     Provides a get method handler.
#     """
#     queryset = Tutorial.objects.all()
#     serializer_class = TutorialSerializer

class ListTutorialView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        tutorial_object = Tutorial.objects.all()
        tutorial_serialize = TutorialSerializer(tutorial_object, many = True)
        return Response(tutorial_serialize.data)
    
    def post(self, request):
        tutorial_serialize = TutorialSerializer(data = request.data)
        if tutorial_serialize.is_valid():
            tutorial_serialize.save()
            return Response(tutorial_serialize.data, status=status.HTTP_201_CREATED)
        return Response(tutorial_serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUpdateTutorialView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Tutorial.objects.get(pk=pk)
        except Tutorial.ObjectDoesNotExist:
            return Response(status.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk):
        tutorial_object = self.get_object(pk)
        tutorial_serialize = TutorialSerializer(tutorial_object)
        return Response(tutorial_serialize.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        tutorial_object = self.get_object(pk)
        tutorial_serialize = TutorialSerializer(tutorial_object, data=request.data)
        if tutorial_serialize.is_valid():
            tutorial_serialize.save()
            return Response(tutorial_serialize.data, status=status.HTTP_200_OK)
        return Response(tutorial_serialize.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        tutorial_object = self.get_object(pk)
        tutorial_object.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


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




# @api_view(['GET', 'POST', 'DELETE'])
# def tutorial_list(request):
#     if request.method == 'GET':
#         tutorials = Tutorial.objects.all()
        
#         title = request.query_params.get('title', None)
#         if title is not None:
#             tutorials = tutorials.filter(title__icontains=title)
        
#         tutorials_serializer = TutorialSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)
#         # 'safe=False' for objects serialization
 
#     elif request.method == 'POST':
#         tutorial_data = JSONParser().parse(request)
#         tutorial_serializer = TutorialSerializer(data=tutorial_data)
#         if tutorial_serializer.is_valid():
#             tutorial_serializer.save()
#             return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         count = Tutorial.objects.all().delete()
#         return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
# @api_view(['GET', 'PUT', 'DELETE'])
# def tutorial_detail(request, pk):
#     try: 
#         tutorial = Tutorial.objects.get(pk=pk) 
#     except Tutorial.DoesNotExist: 
#         return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
#     if request.method == 'GET': 
#         tutorial_serializer = TutorialSerializer(tutorial) 
#         return JsonResponse(tutorial_serializer.data) 
 
#     elif request.method == 'PUT': 
#         tutorial_data = JSONParser().parse(request) 
#         tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
#         if tutorial_serializer.is_valid(): 
#             tutorial_serializer.save() 
#             return JsonResponse(tutorial_serializer.data) 
#         return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
#     elif request.method == 'DELETE': 
#         tutorial.delete() 
#         return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
# @api_view(['GET'])
# def tutorial_list_published(request):
#     tutorials = Tutorial.objects.filter(published=True)
        
#     if request.method == 'GET': 
#         tutorials_serializer = TutorialSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)