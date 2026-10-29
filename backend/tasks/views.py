from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Task
from .serializers import TaskSerializer

@extend_schema_view(
    list=extend_schema(summary="Return all tasks — 200 OK"),
    retrieve=extend_schema(summary="Return one task — 200 OK; 404 if missing"),
    create=extend_schema(summary="Create a task — 201 Created; 400 if invalid"),
    update=extend_schema(summary="Update a task — 200 OK; 400 / 404 as relevant"),
    partial_update=extend_schema(summary="Partial update a task"),
    destroy=extend_schema(summary="Delete a task — 204 No Content; 404 if missing"),
)
class TaskViewSet(viewsets.ModelViewSet):
    """
    Class-Based ModelViewSet implementing the Safaricom Task Manager CRUD API contract.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
