import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('initial', action='store_true', help='load initial data from fixtures')

    def handle(self, *args, **kwargs):
        initial = kwargs.get('initial', False)

        if initial:
            list_file = os.listdir(os.path.join(settings.BASE_DIR, 'api', 'fixtures'))
            for filename in list_file:
                print(f"Load data from: {filename}")
                call_command('loaddata', filename)