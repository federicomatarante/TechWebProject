from django.urls import reverse_lazy
from django.views.generic import CreateView

from GymApp.forms import UserRegistrationForm
from GymApp.models import GymUser



class UserRegistrationView(CreateView):
    model = GymUser
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
