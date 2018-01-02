from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User


class IndexView(generic.ListView):
    model = User
    template_name = 'profiles/index.html'
    context_object_name = 'user_list'


class DetailView(generic.DetailView):
    model = User
    template_name = 'profiles/user_details.html'
