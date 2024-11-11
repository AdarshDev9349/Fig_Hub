from rest_framework import serializers
from .models import Profile, Project
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True, source='user.project_set')
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = ['id','username' ,'user', 'projects']

