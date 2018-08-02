from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from porthole.models import Organization, Location, SwitchStack, Switch, VLAN, Port


#########################################################################
# Helper Utilities
#########################################################################

def sort_ports(ports, order_by):
    if not ports or not order_by:
        return
    if order_by.startswith('p'):
        ports = ports.order_by('label')
    elif order_by.startswith('l'):
        ports = ports.order_by('location')
    elif order_by.startswith('s'):
        ports = ports.order_by('switch', 'switch_port')
    elif order_by.startswith('v'):
        ports = ports.order_by('vlan')
    if len(order_by) == 2 and order_by[1] == '-':
        ports = ports.reverse()
    return ports

def split_label(label):
    alphas = ""
    digits = ""
    for c in label:
        if c.isalpha():
            alphas += c
        elif c.isdigit():
            digits += c
    return (alphas, digits)

#########################################################################
# Generic Views
#########################################################################

def home(request):
    context = {}
    return render(request, 'porthole/home.html', context)

def search(request):
    closets = Location.objects.data_closets()
    ports = None
    closet_number = None
    port_label = None
    if request.POST:
        try:
            if 'closet_number' in request.POST:
                closet_number = request.POST['closet_number']
                closet = Location.objects.filter(number=closet_number).first()
                ports = Port.objects.filter(closet=closet)
            else:
                ports = Port.objects.all()

            if 'port_label' in request.POST:
                port_label = request.POST['port_label']
                alphas, digits = split_label(port_label)
                if alphas:
                    ports = ports.filter(label__istartswith=alphas)
                if digits:
                    ports = ports.filter(label__contains=digits)
        except Exception as e:
            messages.add_message(request, messages.ERROR, f"Error performing search: {e} ")
    order_by = request.GET.get('order_by', 'p')
    ports = sort_ports(ports, order_by)
    context = {
        'closets': closets,
        'ports': ports,
        'order_by': order_by,
        'q_closet': closet_number,
        'q_label': port_label,
    }
    return render(request, 'porthole/search.html', context)

def port_view(request, port_id):
    port = get_object_or_404(Port, id=port_id)
    context = {
        'port': port,
    }
    return render(request, 'porthole/port_view.html', context)

#########################################################################
# Location Views
#########################################################################

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
    order_by = request.GET.get('order_by', 's')
    ports = sort_ports(location.port_set.all(), order_by)
    context = {
        'location': location,
        'order_by': order_by,
        'ports': ports,
    }
    return render(request, 'porthole/location_view.html', context)

#########################################################################
# Switch Views
#########################################################################

def switch_list(request):
    # A data closet is a location with switches in it
    closets = Location.objects.data_closets()
    context = {
        'closets': closets
    }
    return render(request, 'porthole/switch_list.html', context)

def switch_view(request, stack, unit):
    switch = get_object_or_404(Switch, stack__name=stack, unit=unit)
    order_by = request.GET.get('order_by', 's')
    ports = sort_ports(switch.port_set.all(), order_by)
    context = {
        'switch': switch,
        'order_by': order_by,
        'ports': ports,
    }
    return render(request, 'porthole/switch_view.html', context)

#########################################################################
# VLAN Views
#########################################################################

def vlan_list(request):
    vlans = VLAN.objects.all().order_by('tag')
    context = {
        'vlans': vlans,
    }
    return render(request, 'porthole/vlan_list.html', context)

def vlan_view(request, vlan):
    vlan = get_object_or_404(VLAN, tag=vlan)
    order_by = request.GET.get('order_by', 's')
    ports = sort_ports(vlan.port_set.all(), order_by)
    context = {
        'vlan': vlan,
        'order_by': order_by,
        'ports': ports,
    }
    return render(request, 'porthole/vlan_view.html', context)

#########################################################################
# Org Views
#########################################################################

def org_list(request):
    orgs = Organization.objects.all().order_by('name')
    context = {
        'orgs': orgs,
    }
    return render(request, 'porthole/org_list.html', context)


def org_view(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    ports = org.ports()
    context = {
        'org': org,
        'ports': ports,
    }
    return render(request, 'porthole/org_view.html', context)

def org_print(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    context = {
        'org': org,
        'vlan': org.vlan,
    }
    return render(request, 'porthole/org_print.html', context)
