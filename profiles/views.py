from django.shortcuts import render
from django.contrib.auth.models import User
from profiles.serializers import UserDetailSerializer, UserSerializer
from profiles.models import Profile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProfileList(generics.ListCreateAPIView):
    """
    get:
    Returns a list of profiles at low detail.

    post:
    Creates a new User and Profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    
    

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Get details of user with id = {id}. 
    NOTE  user id is different to profile id.
    Always use the user id when fetching data. Profile data is bundled with this
    requests response.

    put:
    Update user details. To update profile details, send them in another dictionary,
    for example {"username": "newname", "profile": {"bio": "cameraguy"}}

    patch:
    Update user details. To update profile details, send them in another dictionary,
    for example {"username": "newname", "profile": {"bio": "cameraguy"}}

    delete:
    Delete user with id = {id}
    """

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)



