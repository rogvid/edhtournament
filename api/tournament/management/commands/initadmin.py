from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = options.get("username", "admin")
            password = options.get("password", "admin")
            email = options.get("email", "admin@admin.com")
            print(f"Creating superuser account for {username}")
            admin = User.objects.create_user(username=username, password=password, email=email)
            admin.is_active = True
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
        else:
            print("Admin accounts can only be initialized if no admin exists")
