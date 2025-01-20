from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
import logging

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Assign user to group'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('group_name', type=str, help='Name of the group')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        group_name = kwargs['group_name']
        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            logger.info(f"User {username} added to group {group_name}")
            self.stdout.write(self.style.SUCCESS(f'User {username} added to group {group_name}'))
        except User.DoesNotExist:
            logger.error(f"User {username} does not exist")
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
        except Group.DoesNotExist:
            logger.error(f"Group {group_name} does not exist")
            self.stdout.write(self.style.ERROR(f'Group {group_name} does not exist'))
