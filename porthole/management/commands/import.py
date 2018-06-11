from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from porthole.models import Location, Switch, VLAN, Port
from porthole.importer import Importer

class Command(BaseCommand):
    help = "Import an Excel file"
    args = "[excel_file]"
    requires_system_checks = True

    def add_arguments(self, parser):
        parser.add_argument('excel_file', nargs='+', type=str)

    def handle(self, *args, **options):
        excel_file = options['excel_file'][0]
        print("Importing '%s'" % excel_file)
        try:
            importer = Importer(excel_file)
            importer.import_data()
        except Exception as e:
            print(str(e))
            raise e
