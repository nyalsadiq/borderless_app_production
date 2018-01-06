from django.views import generic, View
from .models import Project, Requirement
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse


class IndexView(generic.ListView):
    context_object_name = 'project_list'
    template_name='projects/index.html'

    
    def get_queryset(self):
        """
            GET returns queryset of all projects
        """
        return Project.objects.all()

    def post(self, request, *args, **kwargs):
        """
            POST creates a new project with title and description parameters
        """
        project_title = request.POST['project_title']
        description = request.POST['description']

        Project.objects.create(title = project_title, description=description)

        return HttpResponseRedirect(reverse('projects:index'))

class ProjectView(View):
    context_object_name = 'project'
    template_name='projects/details.html'

    def get(self, request, *args, **kwargs):
        """
            Return details of one project
        """
        project_id = kwargs.get('project_id')

        project = get_object_or_404(Project, pk=project_id)
        requirements = Requirement.objects.filter(project=project.id)

        return render(request, 'projects/details.html',{'project':project, 'requirements':requirements})


    def post(self, request, *args, **kwagrs):
        """
            PATCH updates title/description field of specific project
            DELETE deletes specific project
            The request to be used (patch/delete) is posted via the 'field' hidden input
        """
        method = request.POST['method']
        project_id = request.POST['project_id']

        project = get_object_or_404(Project, pk=project_id)

        if (method == 'PATCH'):
            field = request.POST['field']
            new_value = request.POST['new_value']

            if (field == "title"):
                project.title = new_value
                project.save()

            elif (field == "description"):
                project.description = new_value
                project.save()

            else:
                return HttpResponseForbidden("Invalid Request.")

        elif (method == 'DELETE'):
            project.delete()
            return HttpResponseRedirect(reverse('projects:index'))

        else:
            return HttpResponseForbidden("Invalid Request.")

        return HttpResponseRedirect(reverse('projects:detail', args=(project_id,)))


    

    