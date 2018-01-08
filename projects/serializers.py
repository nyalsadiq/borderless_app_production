from rest_framework import serializers
from .models import Project, Requirement

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'location')


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ('text',)

class ProjectDetailSerializer(serializers.ModelSerializer):
    requirements = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'location', 'requirements')
        
    def get_requirements(self, obj):
        project_id = obj.id
        requirements = Requirement.objects.filter(project__id=project_id).values()
        return RequirementSerializer(requirements, many=True).data

