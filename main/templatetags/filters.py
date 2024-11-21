from django import template
import requests

register = template.Library()
@register.filter(name='parse_skin')
def parse_skin(value):
    return value.replace("_"," ").title()


@register.simple_tag
def calculate_profit(lbin, pricepaid, quantity):
    try:
        lbin = int(lbin)
        pricepaid = int(pricepaid)
        quantity = int(quantity)
    except (ValueError, TypeError):
        return "Invalid data"

    return (lbin - pricepaid) * quantity

@register.filter(name='multiply')
def multiply(a,b):
    return a*b

@register.filter(name="formatCoins")
def formatCoins(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}b"  # Convert to billions
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.0f}m"  # Convert to millions
    else:
        return str(value)  # Return the value as a string if it's less than a million

@register.filter('is_skin')
def is_skin(value):
    from main.models import Skin
    return isinstance(value,Skin)

@register.filter('get_head_url')
def get_head_url(username):
    return f"https://mc-heads.net/avatar/{username}/50"