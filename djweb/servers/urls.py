from .views import *
from django.urls import path

urlpatterns = [
    path('list/', servers_list, name = 'servers_list'),
    path('add/', servers_add, name = 'servers_add'),
    path('detail/<int:id>/', servers_detail, name = 'servers_detail'),
    path('change/<int:id>/', servers_change, name = 'servers_change'),
    path('delete/<int:id>/', servers_delete, name = 'servers_delete'),
]