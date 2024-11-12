from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SubscriberForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscribed!')
        else:
            messages.error(request, form.errors)

    return redirect(request.META.get('HTTP_REFERER'))


def send_newsletter():
    subscribers = Subscriber.objects.all()
    subject = 'New Product Launch!'
    message = 'We are excited to announce the launch of our new product. Visit our site for more details.'
    from_email = settings.EMAIL_HOST_USER  # Email konfiguratsiyasidan foydalanamiz

    recipient_list = [subscriber.email for subscriber in subscribers]
    send_mail(subject, message, from_email, recipient_list)
