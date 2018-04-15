from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from profiles.serializers import UserSerializer
from rest_framework import generics

class UserList(generic.ListView):
    model = User
    template_name = 'profiles/index.html'
    
class UserDetail(generic.DetailView):
    model = User
    template_name = 'profiles/user_details.html'



