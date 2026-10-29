from rest_framework import serializers
from .models import Task, TaskStatus

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        min_length=3,
        max_length=100,
        required=True,
        error_messages={
            'required': 'Title is required.',
            'min_length': 'Title must be at least 3 characters.',
            'max_length': 'Title cannot exceed 100 characters.'
        }
    )
    description = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        default='',
        error_messages={
            'max_length': 'Description cannot exceed 500 characters.'
        }
    )
    status = serializers.ChoiceField(
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
        required=False,
        error_messages={
            'invalid_choice': 'Status must be one of: TODO, IN_PROGRESS, DONE.'
        }
    )

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Default the status to TODO when omitted on creation
        if 'status' not in validated_data or not validated_data['status']:
            validated_data['status'] = TaskStatus.TODO
        return super().create(validated_data)
