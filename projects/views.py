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
        project_title = request.POST['project_title']
        description = request.POST['description']

        Project.objects.create(title = project_title, description=description)

        return JsonResponse({'result': 'created'})

class ProjectView(View):
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):
        """
            Return details of one project
        """
        project_id = kwargs.get('project_id')

        
        #response = Project.objects.raw('''SELECT * FROM projects_project 
        #LEFT OUTER JOIN projects_requirement ON projects_project.id = projects_requirement.project_id
        #WHERE projects_requirement.project_id = %s''', [project_id])
        
        project = get_object_or_404(Project, pk=project_id)

        if project:
            serializer = ProjectDetailSerializer(project)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'result': 'no project'})

    def post(self, request, *args, **kwargs):
        """
            PATCH updates title/description field of specific project
            DELETE deletes specific project
            The request to be used (patch/delete) is posted via the 'field' hidden input
        """
        project_id = kwargs.get('project_id')
        
        field = request.POST['field']
        new_value = request.POST['new_value']

        project = get_object_or_404(Project, pk=project_id)

        if (field == "title"):
            project.title = new_value
            project.save()
        elif (field == "description"):
            project.description = new_value
            project.save()
        else:
            return JsonResponse({'result':'invalid'})

        return JsonResponse({'result':'updated'})

    def delete(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        return JsonResponse({'result':'deleted'})


    


    