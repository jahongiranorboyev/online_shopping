from django.contrib import admin

from apps.services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass