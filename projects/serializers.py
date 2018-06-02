from rest_framework import serializers
from .models import Project, Requirement, Comment
import logging

logger = logging.getLogger("Serializer")

class RequirementSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.title')
    class Meta:
        model = Requirement
        fields = ('id','project','text')

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    requirements = RequirementSerializer(many = True, required=False, read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'title','owner','description', 'location','requirements',)

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
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id','title','owner', 'description','location','requirements','comments', 'likes','comment_count')
    
    def get_comment_count(self,obj):
        return Comment.objects.filter(project = obj).count()