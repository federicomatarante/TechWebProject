from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models


class GymUser(AbstractUser):
    weight = models.FloatField(null=True, blank=True, verbose_name='peso')
    height = models.FloatField(null=True, blank=True, verbose_name='altezza')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='data di nascita')
    picture = models.ImageField(null=True, blank=True, verbose_name='foto profilo', upload_to='profile_pics')
