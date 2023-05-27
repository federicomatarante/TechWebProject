from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models


class GymUser(AbstractUser):
    gym_name = models.CharField(max_length=64, null=True, blank=True)
