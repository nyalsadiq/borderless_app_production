from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:project_id>/', views.ProjectView.as_view(), name='detail'),
    #path('create/', views.CreateView.as_view(), name='create'),
]
