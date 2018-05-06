from rest_framework import serializers
from .models import Project, Requirement, Comment
import logging

logger = logging.getLogger("Serializer")

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Project
        fields = ('id', 'title','owner','description', 'location',)


class RequirementSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.title')
    class Meta:
        model = Requirement
        fields = ('id','project','text')

class CommentSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.title')
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Comment
        fields = ('id','project','owner','body')

class ProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    requirements = RequirementSerializer(many=True, required=False, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Project
        fields = ('id','title','owner', 'description','location','requirements','comments', 'likes')