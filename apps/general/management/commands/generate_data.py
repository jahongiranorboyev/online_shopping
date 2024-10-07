import os
import requests

from faker import Faker

from django.conf import settings
from django.utils.timezone import now
from django.core.management import BaseCommand


from apps.abouts.models import About

fake = Faker()

RANDOM_CAT_IMAGE_URL= 'https://api.thecatapi.com/v1/images/search'

class Command(BaseCommand):
    def handle(self, *args, **options):
        print(self.stdout.write(self.style.SUCCESS('Successfully generated fake data')))
        today = now().date()
        if not About.objects.exists():
            image_url = requests.get(url=RANDOM_CAT_IMAGE_URL).json()[0]['url']
            image_name = image_url.split('/')[-1]
            django_filename = f'abouts/images/{today.year}/{today.month}/{today.day}/'
            image_dir =os.path.join(settings.MEDIA_ROOT, django_filename)
            filename = os.path.join(image_dir, image_name)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            with open(filename, 'wb') as image:
                image.write(requests.get(image_url).content)


            About.objects.create(
                title=fake.text(155),
                description=fake.text(255),
                image = os.path.join(django_filename, image_name),

            )
        print(self.stdout.write(self.style.SUCCESS('Done')))
