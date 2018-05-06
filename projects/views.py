from projects.models import Project, Requirement, Comment
from projects.serializers import ProjectSerializer, ProjectDetailSerializer, CommentSerializer, RequirementSerializer
from rest_framework import generics, status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from projects.permissions import IsOwnerOrReadOnly, IsRequestOwnerOrReadOnly
import logging

logger = logging.getLogger('views')

@api_view(['GET'])
def api_root(request, format=None):
    """
    Returns links to the projects and profiles directory.
    """
    return Response({
        'profiles': reverse('profiles:index', request=request, format=format),
        'projects': reverse('projects:index', request=request, format=format)
    })

class IndexView(generics.ListCreateAPIView):
    """
    post:
    Creates a new project instance.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    
    def get(self, request, format=None):
        """
        Returns a list of projects at low detail.
        """
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns details of project with id = {id}

    put:
    Updates various fields of the project with id = {id}
    Cannot be used to update requirements, use the requirements view instead.

    patch:
    Updates various fields of the project with id = {id}
    Cannot be used to update requirements, use the requirements view instead.

    delete:
    Deletes project with id = {id}
    """
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

class RequirementView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns requirement with id = {id}

    put:
    Updates the requirement with id = {id}

    patch:
    Updates the requirement with id = {id}

    delete:
    Deletes the requirement with id = {id}
    """
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsRequestOwnerOrReadOnly)

    def post(self, request, *args, **kwargs):
        """
        Creates a new requirement for project with id = {id}
        Must be owner of project to make a requirement.
        """
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)
    
        serializer = RequirementSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(project = project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReactView(generics.RetrieveUpdateDestroyAPIView):
    """
        put:
        Updates the comment with id = {id}
        Send new text in "body" tag of request body.
        
        patch: 
        Updates the comment with id = {id}
        Send new text in "body" tag of request body.

        delete:
        Deletes the comment with id = {id}
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def get(self, request, *args, **kwargs):
        """
        Leave a like for project with id = {id}.
        Incremements "like" field by 1.
        """
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)    

        likes = project.likes + 1
        serializer = ProjectDetailSerializer(project,data={'likes': likes}, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(status=status.HTTP_202_ACCEPTED)
    
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """
        Leave a comment for project with id = {id}.
        """
    
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)
        owner = request.user

        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(owner = owner, project = project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    