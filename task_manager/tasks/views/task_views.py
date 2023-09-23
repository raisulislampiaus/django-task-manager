from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from tasks.models import Task, Photo
from tasks.serializers import TaskSerializer
from django.db.models import Q
from django.utils.dateparse import parse_date

from rest_framework import status



@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()

        # Filtering by title (case-insensitive search)
        title = request.query_params.get('title', None)
        if title:
            tasks = tasks.filter(title__icontains=title)

     
        created_at = request.query_params.get('created_at', None)
        if created_at:
            created_at_date = parse_date(created_at)
            if created_at_date:
                tasks = tasks.filter(created_at__date=created_at_date)

        # Filtering by due date
        due_date = request.query_params.get('due_date', None)
        if due_date:
            due_date_date = parse_date(due_date)
            if due_date_date:
                tasks = tasks.filter(due_date__date=due_date_date)

        # Filtering by priority
        priority = request.query_params.get('priority', None)
        if priority:
            tasks = tasks.filter(priority=priority)

        # Filtering by completion status
        completed = request.query_params.get('completed', None)
        if completed:
            if completed.lower() == 'true':
                tasks = tasks.filter(completed=True)
            elif completed.lower() == 'false':
                tasks = tasks.filter(completed=False)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()

            # Process and associate uploaded photos with the task
            for file in request.FILES.getlist('photos'):
                photo = Photo(image=file)
                photo.save()
                task.photos.add(photo)

            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
def getProduct(request, pk):
    product = Task.objects.get(id=pk)
    serializer = TaskSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Task.objects.get(id=pk)
    product.delete()
    return Response('Producted Deleted')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Task.objects.get(id=pk)

    
    if 'title' in data:
        product.title = data['title']

    
    if 'description' in data:
        product.description = data['description']

 
    if 'due_date' in data:
        product.due_date = data['due_date']

   
    if 'priority' in data:
        product.priority = data['priority']

    
    if 'completed' in data:
        product.completed = data['completed']

    product.save()

    serializer = TaskSerializer(product, many=False)
    return Response(serializer.data)

