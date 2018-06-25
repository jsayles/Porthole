from django.conf import settings
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from porthole.models import Location, Port, Switch, VLAN


def home(request):
    context = {}
    return render(request, 'porthole/home.html', context)

def locations(request):
    context = {}
    return render(request, 'porthole/location_list.html', context)

def location(request, location):
    context = {}
    return render(request, 'porthole/location_view.html', context)

def switches(request):
    context = {}
    return render(request, 'porthole/switch_list.html', context)

def switch(request, switch):
    context = {}
    return render(request, 'porthole/switch_view.html', context)

def vlans(request):
    context = {}
    return render(request, 'porthole/vlan_list.html', context)

def vlan(request, vlan):
    context = {}
    return render(request, 'porthole/vlan_view.html', context)
