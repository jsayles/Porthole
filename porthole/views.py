from django.conf import settings
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from porthole.models import Location, Port, Switch, VLAN
