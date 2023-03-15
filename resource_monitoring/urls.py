from django.urls import path
from . import views

urlpatterns = [
    path('resource_monitoring/dashboard', views.resources_dashboard, name='resources_dashboard'),
    path('resource_monitoring/stat_plots', views.stat_plots, name='stat_plots'),
]
