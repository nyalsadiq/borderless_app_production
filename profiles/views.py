from django.shortcuts import render
from django.contrib.auth.models import User
from profiles.serializers import UserDetailSerializer, UserSerializer
from profiles.models import Profile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProfileList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)



