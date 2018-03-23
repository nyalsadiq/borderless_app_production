from rest_framework import serializers
from .models import Project, Requirement

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Project
        fields = ('id', 'title','owner','description', 'location')


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ('id','text')


class ProjectDetailSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, required=False)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = ('id','title','owner', 'description','location','requirements')

    def create(self, validated_data):
        if 'requirements' in validated_data:
            requirements_data = validated_data.pop('requirements')
        else:
            requirements_data = []

        project = Project.objects.create(**validated_data)

        for requirement_data in requirements_data:
            Requirement.objects.create(project=project, **requirement_data)

        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)

        if 'requirements' in validated_data:
            requirements_data = validated_data.get('requirements', [])
            for requirement_data in requirements_data:
                req = Requirement(project_id=self.data['id'], **requirement_data)
                req.save()

        instance.save()
        return instance


