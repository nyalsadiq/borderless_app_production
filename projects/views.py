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
    return Response({
        'profiles': reverse('profiles:index', request=request, format=format),
        'projects': reverse('projects:index', request=request, format=format)
    })

class IndexView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

class RequirementView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsRequestOwnerOrReadOnly)

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)
    
        serializer = RequirementSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(project = project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReactView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)    

        likes = project.likes + 1
        serializer = ProjectDetailSerializer(project,data={'likes': likes}, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(status=status.HTTP_202_ACCEPTED)
    
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)
        owner = request.user

        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(owner = owner, project = project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    