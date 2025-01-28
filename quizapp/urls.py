from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views
urlpatterns=[
    path("",views.introduction, name="introduction"),
    path("signup/",views.signup, name="signup"),
    path("signin/",views.signin, name="signin"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("signout/",views.signout,name="signout"),
    path("profile/", views.profile, name='profile'),
    path("quiz1/", views.quiz1, name='quiz1'),
    path("leaders/", views.leaders, name='leaders')
]