from django.contrib import admin

from porthole import models

admin.site.register(models.Location)
admin.site.register(models.SwitchStack)
admin.site.register(models.Switch)
admin.site.register(models.VLAN)
admin.site.register(models.WifiNetwork)
admin.site.register(models.Organization)

class PortAdmin(admin.ModelAdmin):
    def port(self):
        return "%s %s" % (self.closet.number, self.label)

    model = models.Port
    list_display = (port, "location", "switch", "switch_port")
    list_filter = ("closet", "location")
admin.site.register(models.Port, PortAdmin)
