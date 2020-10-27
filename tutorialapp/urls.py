from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import ListProfileView, ListTutorialView

urlpatterns=[
    path('',views.index, name = 'index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update/', views.update, name='update'),
    path('upload_tutorial/', views.upload_tutorial, name='upload_tutorial'),
    path('tutorial/<tutorial_id>/',views.tutorial,name ='tutorial'),
    path('search/', views.search_results, name='search_results'),
    path('api/profile/', ListProfileView.as_view(), name="profile-all"),
    path('api/tutorial/', ListTutorialView.as_view(), name="tutorial-all")
]