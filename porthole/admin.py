from django.contrib import admin

from .models import Location, EthernetPort, Switch

admin.site.register(Location)
admin.site.register(Switch)
admin.site.register(EthernetPort)
