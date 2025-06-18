from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('topup.urls')),
    path('dashboard/', include('topup.dashboard_urls')),
]