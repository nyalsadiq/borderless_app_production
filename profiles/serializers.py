from django.contrib.auth.models import User
from projects.models import Project
from profiles.models import Profile, Skill

from rest_framework import serializers
import logging

logger = logging.getLogger("profiles")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','bio','location')

class SkillSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Skill
        fields = ('id', 'user','text')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username','password','email')
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(many=False,read_only = False)
    skills = SkillSerializer(many=True, read_only=False)
    projects = serializers.HyperlinkedRelatedField(many=True,view_name='projects:detail',queryset=Project.objects.all())

    class Meta:
        model = User
        fields = ('id','username','email','projects','profile', 'skills')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile',None)
        self.update_or_create_profile(instance, profile_data)
        return super(UserDetailSerializer, self).update(instance, validated_data)

    def update_or_create_profile(self, user, profile_data):
        Profile.objects.update_or_create(user=user, defaults=profile_data)


    