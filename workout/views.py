from django.views.generic import DetailView, ListView, CreateView, TemplateView

from GymApp.models import GymUser
from GymApp.widgets import CustomSpanWidget
from base_views import SearchListView
from workout.models import WorkoutPlan, Exercise


class UserWorkoutPlanView(DetailView):
    model = WorkoutPlan
    template_name = 'workout_detail.html'
    context_object_name = 'workoutPlan'

    def get_object(self, queryset=None):
        userRequest = self.request.user
        index = self.request.GET.get('index')
        if index:
            try:
                return WorkoutPlan.objects.filter(user=userRequest).order_by('-created')[int(index)]
            except IndexError:
                return None
        else:
            try:
                return WorkoutPlan.objects.filter(user=userRequest).order_by('-created')[0]
            except IndexError:
                return None


"""class ManageWorkoutsView(ListView):
    model = GymUser
    template_name = 'manage_workouts.html'
    context_object_name = 'gymusers'
    paginate_by = 10
    ordering = ['username']

    def get_queryset(self):
        if self.request.GET.get('search'):
            return GymUser.objects.filter(username__istartswith=self.request.GET['search']).order_by('username')
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_search'] = CustomSpanWidget(
            [(user.username, f'/workout/manage/{user.username}') for user in context['gymusers']]).render('user_search',
                                                                                                          '')
        return context"""


class ManageWorkoutsView(SearchListView):
    template_name = 'manage_workouts.html'

    def __init__(self):
        super().__init__(GymUser, 'username', 'gymusers', 10)

    def search(self, string: str):
        return GymUser.objects.filter(username__istartswith=string)

    def get_url(self, obj) -> str:
        return f'/workout/manage/exercise/{obj.username}'

    def get_name(self, obj) -> str:
        return obj.username


class CreateWorkoutView(TemplateView):
    template_name = 'workout_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = Exercise.objects.all()
        return context
