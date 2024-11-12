from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.newsletter.models import Subscriber
from apps.products.models import Product


@receiver(post_save, sender=Product)
def send_email_new_product(instance,created,**kwargs):
        if created:
                subscribers = Subscriber.objects.all()
                subject = 'New Product Launch!'
                message = 'We are excited to announce the launch of our new product. Visit our site for more details.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [subscriber.email for subscriber in subscribers]
                send_mail(subject, message, from_email, recipient_list)