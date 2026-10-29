from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Task, TaskStatus

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username') or validated_data.get('email'),
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get('username')
        if '@' in username_or_email:
            user = User.objects.filter(email=username_or_email).first()
            if user:
                attrs['username'] = user.username

        data = super().validate(attrs)
        data['token'] = data['access']
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'name': self.user.first_name or self.user.username,
        }
        return data

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
        fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at', 'owner')
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner')

    def create(self, validated_data):
        if 'status' not in validated_data or not validated_data['status']:
            validated_data['status'] = TaskStatus.TODO
        return super().create(validated_data)
