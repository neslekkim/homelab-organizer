import contextlib

from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace_parameter(context, **kwargs):
    query = context["request"].GET.copy()
    for kwarg in kwargs:
        with contextlib.suppress(KeyError):
            query.pop(kwarg)
    query.update(kwargs)
    return mark_safe(query.urlencode())  # noqa: S308


@register.filter
def repeat(string: str, times: int):
    return mark_safe(string * times)  # noqa: S308


@register.simple_tag
def repeat_multi(string: str, times: int, times2: int):
    return mark_safe(string * times * times2)  # noqa: S308
