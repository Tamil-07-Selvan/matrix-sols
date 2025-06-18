from django.urls import path
from . import dashboard_views

urlpatterns = [
    path('', dashboard_views.analytics_dashboard, name='analytics_dashboard'),
]