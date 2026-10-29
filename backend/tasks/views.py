from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Task
from .serializers import (
    TaskSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
)

# ---------------------------------------------------------------------------
# Authentication Views
# ---------------------------------------------------------------------------
@extend_schema(tags=['Authentication'])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

@extend_schema(tags=['Authentication'])
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema(tags=['Authentication'])
class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# ---------------------------------------------------------------------------
# Task ViewSet with User Isolation
# ---------------------------------------------------------------------------
@extend_schema_view(
    list=extend_schema(summary="Return all tasks for current user — 200 OK"),
    retrieve=extend_schema(summary="Return one task — 200 OK; 404 if missing or unauthorized"),
    create=extend_schema(summary="Create a task — 201 Created; 400 if invalid"),
    update=extend_schema(summary="Update a task — 200 OK; 400 / 404 as relevant"),
    partial_update=extend_schema(summary="Partial update a task"),
    destroy=extend_schema(summary="Delete a task — 204 No Content; 404 if missing"),
)
class TaskViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet implementing the Task Manager REST API contract with strict user isolation.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Isolate tasks: only return tasks belonging to the authenticated user
        return Task.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Automatically assign the current user as the task owner
        serializer.save(owner=self.request.user)
