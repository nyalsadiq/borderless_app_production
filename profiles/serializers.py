from django.contrib.auth.models import User
from projects.models import Project
from profiles.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','bio','location')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(many=False, view_name='profiles:detail',queryset=Profile.objects.all())
    class Meta:
        model = User
        fields = ('profile','id','username','email')

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    #profile = ProfileSerializer(many=False,read_only = True)
    projects = serializers.HyperlinkedRelatedField(many=True,view_name='projects:detail',queryset=Project.objects.all())
    class Meta:
        model = User
        fields = ('id','username','email','projects')




    