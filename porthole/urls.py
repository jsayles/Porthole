from django.contrib import admin
from django.urls import path

from porthole import views

app_name = 'porthole'
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),

    path('locations/', views.location_list, name='locations'),
    path('location/<str:location>/', views.location_view, name='location'),

    path('switches/', views.switch_list, name='switches'),
    path('switch/<str:stack>/<int:unit>/', views.switch_view, name='switch'),
    
    path('vlans/', views.vlan_list, name='vlans'),
    path('vlan/<str:vlan>/', views.vlan_view, name='vlan'),

    path('admin/', admin.site.urls),
]
