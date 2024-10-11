from django.core.validators import RegexValidator

check_uzb_number = RegexValidator(
    regex=r'\+998{d}9$',
    message='error',
    code='invalid_number'
    )



