from django.views import generic, View
from .models import Project, Requirement
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
# Create your views here.


#Return list of all projects
class IndexView(generic.ListView):
    context_object_name = 'project_list'
    template_name='projects/index.html'

    def get_queryset(self):
        return Project.objects.all()

    def post(self, request, *args, **kwargs):
        project_title = request.POST['project_title']
        description = request.POST['description']
        Project.objects.create(title = project_title, description=description)
        return HttpResponseRedirect(reverse('projects:index'))

class ProjectView(View):
    context_object_name = 'project'
    template_name='projects/details.html'

    #Return details of one project
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        requirements = Requirement.objects.filter(project=project.id)
        return render(request, 'projects/details.html',{'project':project, 'requirements':requirements})

    #PATCH - Update title/description field
    def post(self, request, *args, **kwagrs):
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


    

    