from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from cryptography.fernet import Fernet

from porthole.models import Location, Switch, VLAN, Port
from porthole.brocade import SwitchStack


def get_auth():
    farnet = Fernet(bytes(settings.BROCADE_KEY, encoding='utf-8'))
    return (
        farnet.decrypt(bytes(settings.BROCADE_USER, encoding='utf-8')).decode(encoding='utf-8'),
        farnet.decrypt(bytes(settings.BROCADE_PASS, encoding='utf-8')).decode(encoding='utf-8'),
    )


class Command(BaseCommand):
    help = "Command the Brocade switch stacks"
    args = ""
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--show_vlans',
            action='store_true',
            dest='show_vlans',
            help='Show the VLAN data from all switch stacks',
        )

    def handle(self, *args, **options):
        if options['show_vlans']:
            self.show_vlans()

    def show_vlans(self):
        farnet = Fernet(bytes(settings.BROCADE_KEY, encoding='utf-8'))
        username = farnet.decrypt(bytes(settings.BROCADE_USER, encoding='utf-8'))
        password = farnet.decrypt(bytes(settings.BROCADE_PASS, encoding='utf-8'))
        for name,ip in settings.BROCADE_SWITCHES:
            stack = SwitchStack(name, ip, username, password)
            stack.print_switches()
            print()
