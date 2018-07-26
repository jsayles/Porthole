from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Count

from cryptography.fernet import Fernet


class Organization(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class LocationManager(models.Manager):

    def data_closets(self):
        # A data closet is a location with switches in it
        return self.annotate(Count('switchstack')).filter(switchstack__count__gt=0).order_by('number')


class Location(models.Model):
    objects = LocationManager()
    number = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=64)
    floor = models.SmallIntegerField()
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" % (self.number, self.name)

    def get_absolute_url(self):
        return reverse('location', kwargs={'location': self.number})

    def get_admin_url(self):
        return reverse('admin:porthole_location_change', args=[self.id])

    class Meta:
        ordering = ['number',]


class SwitchStack(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    ip_address = models.GenericIPAddressField(protocol= 'IPv4', unique=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    port = models.SmallIntegerField(default=22)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    @property
    def raw_username(self):
        if self.username:
            return self.__decrypt_message(self.username)

    @property
    def raw_password(self):
        if self.password:
            return self.__decrypt_message(self.password)

    def __encrypt_message(self, message, encoding='utf-8'):
        farnet = Fernet(bytes(settings.BROCADE_KEY, encoding=encoding))
        return farnet.encrypt(bytes(message, encoding=encoding))

    def __decrypt_message(self, message, encoding='utf-8'):
        farnet = Fernet(bytes(settings.BROCADE_KEY, encoding=encoding))
        return farnet.decrypt(bytes(message, encoding=encoding))

    def __str__(self):
        return self.name


class Switch(models.Model):
    unit = models.SmallIntegerField()
    make = models.CharField(max_length=64, null=True, blank=True)
    model = models.CharField(max_length=64, null=True, blank=True)
    port_count = models.SmallIntegerField(null=True, blank=True)
    stack = models.ForeignKey(SwitchStack, on_delete=models.CASCADE)

    def __str__(self):
        return "%s-%d" % (self.stack.name, self.unit)

    @property
    def location(self):
        return self.stack.location

    def get_absolute_url(self):
        return reverse('switch', kwargs={'stack': self.stack.name, 'unit':self.unit})

    def get_admin_url(self):
        return reverse('admin:porthole_switch_change', args=[self.id])

    class Meta:
        ordering = ['stack', 'unit']


class VLAN(models.Model):
    tag = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=64, null=True, blank=True)
    ip_range = models.CharField(max_length=32, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

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

    def module_id(self):
        # STACKID/SLOT/PORT
        # SLOT = 1 = Ethernet
        return "%d/1/%d" % (self.switch.unit, self.switch_port)

    def get_absolute_url(self):
        return reverse('port', kwargs={'port_id': self.id})

    def get_admin_url(self):
        return reverse('admin:porthole_port_change', args=[self.id])

    class Meta:
        ordering = ['closet__number', 'label']


class WifiNetwork(models.Model):
    ssid = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (self.ssid, self.vlan)
