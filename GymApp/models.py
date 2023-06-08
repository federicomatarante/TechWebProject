from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models


class Notifications(models.Model):
    bullettinboard = models.BooleanField(default=False, verbose_name='bacheca')
    workout = models.BooleanField(default=False, verbose_name='allenamento')
    mealplan = models.BooleanField(default=False, verbose_name='piano alimentare')


class GymUser(AbstractUser):
    weight = models.FloatField(null=True, blank=True, verbose_name='peso')
    height = models.FloatField(null=True, blank=True, verbose_name='altezza')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='data di nascita')
    picture = models.ImageField(null=True, blank=True, verbose_name='foto profilo', upload_to='profile_pics')
    notifications = models.OneToOneField(Notifications, on_delete=models.CASCADE, verbose_name='notifiche',
                                         default=Notifications.objects.create)


class Mail(models.Model):
    email = models.EmailField(verbose_name='email')
    title = models.CharField(max_length=100, verbose_name='titolo')
    message = models.TextField(verbose_name='messaggio')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data di creazione'   )