from projects.models import Project, Requirement
from projects.serializers import ProjectSerializer, ProjectDetailSerializer
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class IndexView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer

    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer

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

    


