from django.contrib import admin

from apps.features.models import Feature, FeatureValue


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass


@admin.register(FeatureValue)
class FeatureValueAdmin(admin.ModelAdmin):
    pass
