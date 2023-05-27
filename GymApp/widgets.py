from typing import Tuple, List

from django.forms.widgets import Widget
from django.template.loader import render_to_string


class CustomSpanWidget(Widget):

    def __init__(self, items: List[Tuple[str, str]], attrs=None):
        super().__init__(attrs)
        self.items = items

    def render(self, name, value, attrs=None, renderer=None):
        context = {
            'attrs': attrs,
            'items': self.items
        }
        return render_to_string('search_list.html', context)
