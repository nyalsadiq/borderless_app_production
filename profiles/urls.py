from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileList.as_view(), name='index'),
    path('<int:pk>/', views.ProfileDetail.as_view(), name='detail'),
    path('<int:pk>/skill/', views.SkillView.as_view(), name='skill'),
    path('me/', views.get_profile_with_token, name='me'),
]
