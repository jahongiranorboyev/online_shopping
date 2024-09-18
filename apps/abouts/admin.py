from apps.abouts.models import About
from django.contrib import admin


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    pass
