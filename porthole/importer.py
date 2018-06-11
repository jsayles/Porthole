from openpyxl import load_workbook

from django.conf import settings
from django.utils.timezone import localtime, now

from porthole.models import Location, Switch, VLAN, Port


LOCATIONS = "Locations"
SWITCHES = "Switches"
VLANS = "VLANs"
PORTS = "Ports"


class Importer(object):

    def __init__(self, file_name):
        self.workbook = load_workbook(filename = file_name)
        for sheet in [LOCATIONS, SWITCHES, VLANS, PORTS]:
            if not sheet in self.workbook.sheetnames:
                raise Exception("'%s' Sheet Not Found!" % sheet)

    def import_data(self):
        self.import_locations()

    def import_locations(self):
        sheet = self.workbook[LOCATIONS]

        # I should get these from the first row but for now I'm
        # going to simply hardcode them to the specific column
        col_number = 0
        col_name = 1

        row_number = 0
        for row in sheet.iter_rows():
            row_number = row_number + 1
            # Skip the first row
            if row_number == 1:
                continue
            number = str(row[col_number].value)
            name = str(row[col_name].value)
            floor = int(number[0])
            # print("Row %d: number: %s, name: %s, floor: %d" % (row_number, number, name, floor))
            location = Location.objects.filter(number=number).first()
            if location:
                location.name = name
                location.floor = floor
            else:
                location = Location(number=number, name=name, floor=floor)
            location.save()
