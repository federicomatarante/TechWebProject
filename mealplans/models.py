from django.db import models


class MealPlan(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    expected_end_date = models.DateTimeField()
    actual_end_date = models.DateTimeField(null=True)
    user = models.ForeignKey('GymApp.GymUser', on_delete=models.CASCADE, related_name='mealPlans')

    def save(self, *args, **kwargs):
        if self.pk is None:
            MealPlan.objects.filter(user=self.user).exclude(pk=self.pk).order_by('-creation_date').update(
                actual_end_date=self.creation_date)
        super().save(*args, **kwargs)


class MealDay(models.Model):
    day = models.IntegerField()
    mealPlan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='mealDays')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Meal(models.Model):
    name = models.CharField(max_length=30)
    mealDay = models.ForeignKey(MealDay, on_delete=models.CASCADE, related_name='meals')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    quantityType = models.CharField(max_length=30)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='ingredients')
