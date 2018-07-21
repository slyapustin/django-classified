from decimal import Decimal as D
from decimal import InvalidOperation

from babel.numbers import format_currency
from django import template
from django.conf import settings
from django.utils.translation import get_language, to_locale

from django_classified.settings import CURRENCY

register = template.Library()


@register.filter(name='currency')
def currency(value, currency=None):
    """
    Format decimal value as currency
    """
    try:
        value = D(value)
    except (TypeError, InvalidOperation):
        return ""

    # Using Babel's currency formatting
    # http://babel.pocoo.org/en/latest/api/numbers.html#babel.numbers.format_currency

    kwargs = {
        'currency': currency or CURRENCY,
        'locale': to_locale(get_language() or settings.LANGUAGE_CODE)
    }

    return format_currency(value, **kwargs)
