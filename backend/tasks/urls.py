from django.urls import re_path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    TaskViewSet,
    RegisterView,
    LoginView,
    CurrentUserView,
)

task_list = TaskViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

task_detail = TaskViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # Authentication Endpoints
    re_path(r'^auth/register/?$', RegisterView.as_view(), name='auth-register'),
    re_path(r'^auth/login/?$', LoginView.as_view(), name='auth-login'),
    re_path(r'^auth/refresh/?$', TokenRefreshView.as_view(), name='auth-refresh'),
    re_path(r'^auth/me/?$', CurrentUserView.as_view(), name='auth-me'),

    # Task Endpoints (User Isolated)
    re_path(r'^tasks/?$', task_list, name='task-list'),
    re_path(r'^tasks/(?P<pk>[0-9]+)/?$', task_detail, name='task-detail'),
]
