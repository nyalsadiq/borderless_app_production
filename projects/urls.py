from django.urls import path
from . import views
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
#(cache_page(CACHE_TTL))

app_name = 'projects'
urlpatterns = [
    path('', (views.IndexView.as_view()), name='index'),
    path('<int:pk>/', (views.ProjectView.as_view()), name='detail'),
    path('<int:pk>/react/', views.ReactView.as_view(), name='react'),
    path('<int:pk>/requirement/', views.RequirementView.as_view(), name='requirement'),
    path('findjobs/', views.get_reccomended_jobs,name='jobs')
]
