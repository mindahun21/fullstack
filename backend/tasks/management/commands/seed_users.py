from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Task

class Command(BaseCommand):
    help = 'Seeds initial test users and isolated tasks'

    def handle(self, *args, **options):
        # User 1
        u1, _ = User.objects.get_or_create(
            username='user1@example.com',
            defaults={'email': 'user1@example.com', 'first_name': 'Abebe'}
        )
        u1.set_password('password123')
        u1.save()

        # User 2
        u2, _ = User.objects.get_or_create(
            username='user2@example.com',
            defaults={'email': 'user2@example.com', 'first_name': 'Minda'}
        )
        u2.set_password('password123')
        u2.save()

        # Tasks for User 1
        Task.objects.get_or_create(
            title="User 1 - Prepare Network Report",
            defaults={'description': 'Compile latency figures', 'status': 'TODO', 'owner': u1}
        )

        # Tasks for User 2
        Task.objects.get_or_create(
            title="User 2 - Review Pull Requests",
            defaults={'description': 'Code review for core microservices', 'status': 'IN_PROGRESS', 'owner': u2}
        )

        self.stdout.write(self.style.SUCCESS("Seeded users: user1@example.com and user2@example.com (password: password123)"))
