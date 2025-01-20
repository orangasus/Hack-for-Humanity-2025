# management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import ExtendedUser  

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Create a group
        group, created = Group.objects.get_or_create(name='MyGroup')

        # Create permissions
        content_type = ContentType.objects.get_for_model(ExtendedUser)
        permission = Permission.objects.create(
            codename='can_view_mymodel',
            name='Can View MyModel',
            content_type=content_type,
        )

        # Assign permissions to group
        group.permissions.add(permission)
        self.stdout.write(self.style.SUCCESS('Successfully created group and permissions'))
