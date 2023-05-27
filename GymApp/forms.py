from django import forms
from django.contrib.auth.forms import UserCreationForm

from GymApp.models import GymUser


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = GymUser
        fields = ('username', 'first_name','last_name','email', 'password1', 'password2')
