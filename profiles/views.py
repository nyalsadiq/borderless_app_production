from django.shortcuts import render
from django.contrib.auth.models import User
from profiles.serializers import UserDetailSerializer, UserSerializer, SkillSerializer
from profiles.models import Profile, Skill
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from projects.permissions import IsOwnerOrReadOnly, IsSkillOwnerOrReadOnly, IsProfileOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status, permissions, filters
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.reverse import reverse

logger = logging.getLogger('views')

class ProfileList(generics.ListCreateAPIView):
    """
    get:
    Returns a list of profiles at low detail.

    post:
    Creates a new User and Profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SkillView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns skill with id = {id}

    put:
    Updates skill with id = {id}

    patch:
    Updates skill with id = {id}

    delete:
    Deletes skill with id = {id}

    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,IsSkillOwnerOrReadOnly)

    def post(self, request, *args, **kwargs):
        """
        Creates a new skill for authenticated user.
        Must be owner of user to make a skill.
        Do not need to send the correct user id in get request
        (just use any number)
        """
        user = request.user
        serializer = SkillSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = (IsAuthenticatedOrReadOnly,IsProfileOwnerOrReadOnly)

@api_view(['get'])
@permission_classes((permissions.IsAuthenticated,))
def get_profile_with_token(request):

    user = User.objects.get(username=request.user)
    serializer = UserDetailSerializer(user, context={'request':request})
   
    return Response(serializer.data, status=status.HTTP_200_OK)