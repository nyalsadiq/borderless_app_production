from projects.models import Project, Requirement, Comment
from projects.serializers import ProjectSerializer, ProjectDetailSerializer, CommentSerializer
from rest_framework import generics, status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from projects.permissions import IsOwnerOrReadOnly


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

    def delete(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        deletion_type = data.get('type', "")

        if deletion_type == "project":
            project_id = kwargs.get('pk')
            project = get_object_or_404(Project, pk=project_id)
            project.delete()
        elif deletion_type == "requirement":
            requirement_id = kwargs.get('pk')
            requirement = get_object_or_404(Requirement, pk=requirement_id)
            requirement.delete()
        else:
            return Response({"error":"You must provide the deletion type"}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

class ReactView(APIView):
    
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

    