from django.contrib import admin

from porthole.models import Location, SwitchStack, Switch, VLAN, Port

admin.site.register(Location)
admin.site.register(SwitchStack)
admin.site.register(Switch)
admin.site.register(VLAN)

class PortAdmin(admin.ModelAdmin):
    def port(self):
        return "%s %s" % (self.closet.number, self.label)

    model = Port
    list_display = (port, "location", "switch", "switch_port")
    list_filter = ("closet", "location")
admin.site.register(Port, PortAdmin)
