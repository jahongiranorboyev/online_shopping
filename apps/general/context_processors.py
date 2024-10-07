from apps.general.models import General, GeneralSocialMedia
from apps.wishlist.models import Wishlist


def general_context(request):
    context = {
        'general': General.objects.all(),
        'general_social_media': GeneralSocialMedia.objects.all(),
        'wishlist': Wishlist.objects.all(),
    }
    return context