from django.urls import path

from apps.newsletter.views import subscribe

app_name = 'subscribers'
urlpatterns = [
    path('', subscribe, name='subscribe'),
]
