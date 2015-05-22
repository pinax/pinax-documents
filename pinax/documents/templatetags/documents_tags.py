from django.template import Library

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
