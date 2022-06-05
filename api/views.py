from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import ProjectSerializer

from projects.models import Project

from api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {"GET": "/api/projects"},
        {"GET": "/api/projects/id"},
        {"POST": "/api/projects/id/vote"},
        {"POST": '/api/users/token'},
        {"POST": '/api/users/token/refresh'}
    ]
    # JsonResponse returns a sindle dictionary, safe = False lets Jsonresponse to return more than only a dictionary, a list of dictionary
    return Response(routes)

# Serializer converts complex data such as query sets to JSONObjects


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)
