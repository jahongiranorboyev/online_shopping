from django.contrib import admin

from apps.newsletter.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass
