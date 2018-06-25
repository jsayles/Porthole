from django.contrib import admin
from django.urls import path

from porthole import views

app_name = 'porthole'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('locations', views.locations, name='locations'),
    path('location/<int:location>/', views.location, name='location'),
    path('switches', views.switches, name='switches'),
    path('switch/<int:switch>/', views.switch, name='switch'),
    path('vlans', views.vlans, name='vlans'),
    path('vlan/<int:vlan>/', views.vlan, name='vlan'),
]
