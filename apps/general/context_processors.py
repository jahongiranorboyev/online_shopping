from apps.general.models import General, GeneralSocialMedia
from apps.products.models import Product



def general_context(request):
    context = {
        'general': General.objects.all(),
        'general_social_media': GeneralSocialMedia.objects.all(),
        'currency':request.session.get('currency',Product.DEFAULT_CURRENCY),
        'currency_list':Product.Currency.labels,
    }
    return context