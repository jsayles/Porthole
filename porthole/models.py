from django.db import models
from django.conf import settings


class Location(models.Model):
    name = models.CharField(max_length=64)
    floor = models.CharField(max_length=1)
    number = models.CharField(max_length=5)
    door = models.CharField(max_length=5, null=True, blank=True)


class Switch(models.Model):
    label = models.CharField(max_length=64)
    make = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    port_count = models.SmallIntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class EthernetPort(models.Model):
    label = models.CharField(max_length=4)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
    switch_port = models.SmallIntegerField(null=True, blank=True)
    vlan = models.CharField(max_length=16)
