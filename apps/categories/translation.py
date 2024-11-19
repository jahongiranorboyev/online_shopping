from modeltranslation.translator import TranslationOptions, register
from apps.categories.models import Category


@register(Category)
class CategoriesTranslationOptions(TranslationOptions):
    """
    Translation options for the Category model.

    This class specifies which fields of the Category model should be
    translated for multilingual support. In this case, only the 'name' field
    will be translatable.

    Fields:
        name (str): The name of the category, which will be translated.
    """
    fields = ('name',)

