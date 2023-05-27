from django import template as t
from django.template.loader import get_template

register = t.Library()


@register.simple_tag()
def logged_header(highlighted_index: int):
    template = get_template('loggedheader.html')
    context = {
        'highlighted_index': highlighted_index
    }
    return template.render(context)

