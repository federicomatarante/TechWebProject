from abc import ABC

from django.db.models import QuerySet
from django.views.generic import ListView

from GymApp.widgets import CustomSpanWidget


class SearchListView(ListView, ABC):

    def __init__(self, model, ordering: str, context_object_name: str, paginate_by: int = 10):
        super().__init__()
        self.model = model
        self.ordering = ordering
        self.context_object_name = context_object_name
        self.paginate_by = paginate_by

    def get_queryset(self):
        if self.request.GET.get('search'):
            return self.search(self.request.GET['search']).order_by(self.ordering)
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = CustomSpanWidget(
            [(self.get_name(item), self.get_url(item)) for item in self.object_list]).render('search',
                                                                                       '')
        return context

    def search(self, string: str) -> QuerySet:
        pass

    def get_url(self, obj) -> str:
        pass

    def get_name(self,obj)-> str:
        pass