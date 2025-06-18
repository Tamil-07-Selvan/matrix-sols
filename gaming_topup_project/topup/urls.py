from django.urls import path
from . import views

urlpatterns = [
    path('topup/', views.create_topup_order, name='create_topup_order'),
]