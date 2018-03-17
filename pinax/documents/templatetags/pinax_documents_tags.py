from django.template import Library
from django.utils.html import conditional_escape

from ..utils import convert_bytes

register = Library()


@register.filter
def can_share(member, user):
    if member is None:
        return False
    return member.can_share(user)


@register.filter
def readable_bytes(bytes):
    return convert_bytes(bytes)


@register.simple_tag
def user_display(user):
    try:
        # Use django-user-accounts display function if available
        from account.utils import user_display as account_user_display
        return conditional_escape(account_user_display(user))
    except ImportError:
        return conditional_escape(user.username)
