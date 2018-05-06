from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileList.as_view(), name='index'),
    path('<int:pk>/', views.ProfileDetail.as_view(), name='detail')
]
