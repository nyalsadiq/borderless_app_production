from django.views import generic, View
from .models import Project, Requirement
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse, QueryDict
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import ProjectSerializer,ProjectDetailSerializer,RequirementSerializer

class IndexView(View):
    context_object_name = 'project_list'

    def get(self, request):
        """
            GET returns queryset of all projects
        """
        project_list = Project.objects.all()

        if project_list:
            serializer = ProjectSerializer(project_list, many=True)
            return JsonResponse(serializer.data,safe=False)
        else:
            return JsonResponse({'result': 'no projects'})
            
    def post(self, request, *args, **kwargs):
        """
            POST creates a new project with title and description parameters
        """
        data = JSONParser().parse(request)
        serializer = ProjectDetailSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        serializer.save()

        return JsonResponse(serializer.data, status=201)

class ProjectView(View):
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):
        """
            Return details of one project
        """
        project_id = kwargs.get('project_id')

        project = get_object_or_404(Project, pk=project_id)

        serializer = ProjectDetailSerializer(project)
        return JsonResponse(serializer.data, safe=False)
    

    def patch(self, request, *args, **kwargs):
        """
            PATCH updates title/description field of specific project
            DELETE deletes specific project
            The request to be used (patch/delete) is posted via the 'field' hidden input
        """
        project_id = kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)

        data = JSONParser().parse(request)
        serializer = ProjectDetailSerializer(project, data=data, partial=True)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=404)

        serializer.save()
        return JsonResponse(serializer.data)

    def delete(self, request, *args, **kwargs):
        data = JSONParser().parse(request)

        deletion_type = data.get('type', "")

        if deletion_type == "project":
            project_id = kwargs.get('project_id')
            project = get_object_or_404(Project, pk=project_id)
            project.delete()
        elif deletion_type == "requirement":
            requirement_id = kwargs.get('project_id')
            requirement = get_object_or_404(Requirement, pk=requirement_id)
            requirement.delete()
        else:
            return JsonResponse({"error":"You must provide the deletion type"}, status=404)

        return HttpResponse(status=204)


    


    