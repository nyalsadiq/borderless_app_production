"""borderlessapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import include
from projects import views
from profiles import views as profile_views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', views.api_root),
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls')),
    path('projects/', include('projects.urls')),
    path('login/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('docs/', include_docs_urls(title='Borderless API')),
]
