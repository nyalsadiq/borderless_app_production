from rest_framework import permissions
from .models import Project, Requirement
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger('permissions')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self,request,view,obj):
        # Read permissions are allowed to any request
        # So we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the snippet
        return obj.owner == request.user

class IsRequestOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        req_key = obj.id
        logger.error(req_key)
        requirement = get_object_or_404(Requirement, pk=req_key)
        project = get_object_or_404(Project, pk=requirement.project_id)

        return project.owner == request.user
        