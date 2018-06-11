from django.contrib import admin

from porthole.models import Location, Port, Switch, VLAN

admin.site.register(Location)
admin.site.register(Switch)
admin.site.register(VLAN)
admin.site.register(Port)
