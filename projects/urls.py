from django.urls import path
from . import views
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings

#CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
#(cache_page(CACHE_TTL))
#def cacheops_prefix(query):
#    return 'borderless'

app_name = 'projects'
urlpatterns = [
    path('', (views.IndexView.as_view()), name='index'),
    path('<int:pk>/', (views.ProjectView.as_view()), name='detail'),
    path('<int:pk>/comment/', views.CommentView.as_view(), name='comment'),
    path('<int:pk>/like/', views.like_or_unlike,name='like'),
    path('<int:pk>/requirement/', views.RequirementView.as_view(), name='requirement'),
    path('findjobs/', views.get_reccomended_jobs,name='jobs')
]
