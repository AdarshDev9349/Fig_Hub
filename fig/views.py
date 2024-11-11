# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Profile, Project
from .serializers import ProfileSerializer, ProjectSerializer
from django.db.models import Q
from rest_framework import status
import os
import requests

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')

    if password != password_confirm:
        return Response({'error': 'Passwords do not match'}, status=400)

    try:
        validate_password(password)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'}, status=201)
    except ValidationError as e:
        return Response({'error': e.messages}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        profile, _ = Profile.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': ProfileSerializer(profile).data
        }, status=200)
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.auth.delete()
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)


from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_view(request):
   
    if request.method == 'POST':
        
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle GET request
    profile = get_object_or_404(Profile, user=request.user)
    serializer = ProfileSerializer(profile)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_project(request):
    figma_url = request.data.get('figma_url')
    project_name = request.data.get('project_name')

    if figma_url and project_name:
        try:
            file_key = figma_url.split('/file/')[1].split('/')[0]
            api_url = f'https://api.figma.com/v1/images/{file_key}'
            headers = {'X-FIGMA-TOKEN': os.getenv('FIGMA_TOKEN')}
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                image_url = response.json()['images']
                project = Project.objects.create(
                    user=request.user,
                    name=project_name,
                    figma_url=figma_url,
                    image_url=image_url
                )
                return Response(ProjectSerializer(project).data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    return Response({'error': 'Invalid data'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.query_params.get('query', '')
    if query:
        users = Profile.objects.filter(
            Q(user__username__icontains=query) | Q(user__first_name__icontains=query)
        )
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'No search query provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request, user_id):
    try:
        profile = Profile.objects.get(user__id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)