from django.shortcuts import render
from django.views import generic
from .models import Project
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'projects/index.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        return Project.objects.order_by('-title')
    