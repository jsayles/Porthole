from django.conf import settings
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Count

from porthole.models import Location, Port, Switch, VLAN


def home(request):
    context = {}
    return render(request, 'porthole/home.html', context)

def location_list(request):
    locations = (
        (0, Location.objects.filter(floor=0)),
        (1, Location.objects.filter(floor=1)),
        (2, Location.objects.filter(floor=2)),
    )
    context = {
        'locations': locations,
    }
    return render(request, 'porthole/location_list.html', context)

def location_view(request, location):
    location = get_object_or_404(Location, number=location)
    ports = location.port_set.all().order_by('switch')
    context = {
        'location': location,
        'ports': ports,
    }
    return render(request, 'porthole/location_view.html', context)

def switch_list(request):
    # A data closet is a location with switches in it
    closets = Location.objects.annotate(Count('switch')).filter(switch__count__gt=0).order_by('number')
    context = {
        'closets': closets
    }
    return render(request, 'porthole/switch_list.html', context)

def switch_view(request, switch):
    switch = get_object_or_404(Switch, label=switch)
    ports = switch.port_set.all()
    context = {
        'switch': switch,
        'ports': ports,
    }
    return render(request, 'porthole/switch_view.html', context)

def vlan_list(request):
    vlans = VLAN.objects.all().order_by('tag')
    context = {
        'vlans': vlans,
    }
    return render(request, 'porthole/vlan_list.html', context)

def vlan_view(request, vlan):
    vlan = get_object_or_404(VLAN, tag=vlan)
    ports = vlan.port_set.all()
    context = {
        'vlan': vlan,
        'ports': ports,
    }
    return render(request, 'porthole/vlan_view.html', context)
