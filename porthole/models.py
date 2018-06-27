from django.db import models
from django.conf import settings
from django.urls import reverse


class Location(models.Model):
    number = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=64)
    floor = models.SmallIntegerField()

    def __str__(self):
        return "%s: %s" % (self.number, self.name)

    def get_absolute_url(self):
        return reverse('location', kwargs={'location': self.number})

    def get_admin_url(self):
        return reverse('admin:porthole_location_change', args=[self.id])

    class Meta:
        ordering = ['number',]


class Switch(models.Model):
    label = models.CharField(max_length=64, unique=True)
    make = models.CharField(max_length=64, null=True, blank=True)
    model = models.CharField(max_length=64, null=True, blank=True)
    port_count = models.SmallIntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('switch', kwargs={'switch': self.label})

    def get_admin_url(self):
        return reverse('admin:porthole_switch_change', args=[self.id])

    class Meta:
        ordering = ['label',]


class VLAN(models.Model):
    tag = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=64, null=True, blank=True)
    ip_range = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return "%s: %s" % (self.tag, self.name)

    def get_absolute_url(self):
        return reverse('vlan', kwargs={'vlan': self.tag})

    def get_admin_url(self):
        return reverse('admin:porthole_vlan_change', args=[self.id])
    
    class Meta:
        ordering = ['tag',]


class Port(models.Model):
    label = models.CharField(max_length=4)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    closet = models.ForeignKey(Location, related_name="+", on_delete=models.CASCADE)
    switch = models.ForeignKey(Switch, null=True, blank=True, on_delete=models.CASCADE)
    switch_port = models.SmallIntegerField(null=True, blank=True)
    vlan = models.ForeignKey(VLAN, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.closet.number, self.label)

    # def get_absolute_url(self):
    #     return reverse('member:receipt', kwargs={'bill_id': self.id})

    def get_admin_url(self):
        return reverse('admin:porthole_port_change', args=[self.id])

    class Meta:
        ordering = ['closet__number', 'label']
