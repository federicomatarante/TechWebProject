from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from base_views import SearchListView
from .models import Exercise, ExerciseSet


class ExerciseListView(SearchListView):
    model = Exercise
    template_name = 'exercise_list.html'
    context_object_name = 'exercises'

    def __init__(self):
        super().__init__(Exercise, 'name', 'exercises')

    def search(self, string: str) -> QuerySet:
        return self.model.objects.filter(name__icontains=string)

    def get_url(self, obj) -> str:
        return reverse_lazy('update_exercise', kwargs={'pk': obj.pk})

    def get_name(self, obj) -> str:
        return obj.name


class ExerciseCreateView(CreateView):
    model = Exercise
    fields = ['name', 'description']
    template_name = 'exercise_create.html'
    success_url = reverse_lazy('exercise_list')



class ExerciseUpdateView(UpdateView):
    model = Exercise
    template_name = 'exercise_update.html'
    success_url = reverse_lazy('exercise_list')
    fields = ['name', 'description']
    context_object_name = 'exercise'


@require_POST
def delete_exercise(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if ExerciseSet.objects.filter(exercise=exercise).exists():
        return HttpResponse(status=409, content='Non puoi eliminare un esercizio che è presente in un workout')
    exercise.delete()
    return HttpResponse(status=204)
