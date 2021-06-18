from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('nm_marketplace.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
