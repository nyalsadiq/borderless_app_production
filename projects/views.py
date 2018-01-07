from django.views import generic, View
from .models import Project, Requirement
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse, QueryDict
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


class IndexView(View):
    context_object_name = 'project_list'

    def get(self, request):
        """
            GET returns queryset of all projects
        """
        project_list = Project.objects.all()
        response = serializers.serialize("json", project_list)
        return HttpResponse(response, content_type='application/json')

    
    def post(self, request, *args, **kwargs):
        """
            POST creates a new project with title and description parameters
        """
        project_title = request.POST['project_title']
        description = request.POST['description']

        Project.objects.create(title = project_title, description=description)

        return JsonResponse({'status': 'created'})

class ProjectView(View):
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):
        """
            Return details of one project
        """
        project_id = kwargs.get('project_id')

        project = get_object_or_404(Project, pk=project_id)
        requirements = Requirement.objects.filter(project=project.id)

        project_json = serializers.serialize("json", [project])
        requirements_json = serializers.serialize("json", requirements)

        response = [project_json,requirements_json]
        return HttpResponse(response, content_type='application/json')
    

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
            return JsonResponse({'status':'invalid'})

        return JsonResponse({'status':'updated'})

    def delete(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        return JsonResponse({'status':'deleted'})


    


    