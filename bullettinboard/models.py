from django.db import models

from GymApp.models import GymUser


class Message(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)
    author = models.ForeignKey(GymUser, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
