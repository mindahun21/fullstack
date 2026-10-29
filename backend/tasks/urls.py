from django.urls import path, re_path
from .views import TaskViewSet

# Map viewset actions to explicit URL patterns supporting both trailing and non-trailing slashes
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
    re_path(r'^tasks/?$', task_list, name='task-list'),
    re_path(r'^tasks/(?P<pk>[0-9]+)/?$', task_detail, name='task-detail'),
]
