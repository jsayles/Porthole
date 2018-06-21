from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from cryptography.fernet import Fernet

from porthole.models import Location, Switch, VLAN, Port
from porthole.brocade import SwitchStack


class Command(BaseCommand):
    help = "Command the Brocade switch stacks"
    args = ""
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--print_stacks',
            action='store_true',
            dest='print_stacks',
            help='Show the VLAN data from all switch stacks',
        )

    def handle(self, *args, **options):
        if options['print_stacks']:
            self.print_stacks()

    def print_stacks(self):
        username = self.decrypt_message(settings.BROCADE_USER)
        password = self.decrypt_message(settings.BROCADE_PASS)
        for name,ip in settings.BROCADE_SWITCHES:
            stack = SwitchStack(name, ip, username, password)
            stack.print_stack()
            print()

    def encrypt_message(self, message, encoding='utf-8'):
        farnet = Fernet(bytes(settings.BROCADE_KEY, encoding=encoding))
        return farnet.encrypt(bytes(message, encoding=encoding))

    def decrypt_message(self, message, encoding='utf-8'):
        farnet = Fernet(bytes(settings.BROCADE_KEY, encoding=encoding))
        return farnet.decrypt(bytes(message, encoding=encoding))
