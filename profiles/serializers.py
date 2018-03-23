from django.contrib.auth.models import User
from projects.models import Project
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username','projects')
