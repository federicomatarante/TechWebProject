from django.db import models

from GymApp.models import GymUser


class Exercise(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='exercise_images', blank=True)  # TODO ?


class WorkoutPlan(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    expected_end_date = models.DateTimeField()
    actual_end_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(GymUser, related_name='workout_plans', on_delete=models.CASCADE)


class WorkoutDay(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='workout_days')


class ExerciseSet(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField()
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='exercise_sets')
