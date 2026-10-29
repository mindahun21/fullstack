from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator

class TaskStatus(models.TextChoices):
    TODO = 'TODO', 'TODO'
    IN_PROGRESS = 'IN_PROGRESS', 'IN_PROGRESS'
    DONE = 'DONE', 'DONE'

class Task(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)],
        help_text="Required; 3-100 characters"
    )
    description = models.CharField(
        max_length=500,
        blank=True,
        default='',
        validators=[MaxLengthValidator(500)],
        help_text="Optional; maximum 500 characters"
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
        help_text="TODO, IN_PROGRESS, DONE; default TODO"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}: {self.title} ({self.status})"
