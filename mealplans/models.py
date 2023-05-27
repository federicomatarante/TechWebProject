from django.db import models

"""
 Dieta {
    MealDay1 {
        WeekDay: //,
        MealTime1 {
            Meal1 {

            },
            Meal2 {

            },
        },
        weekDay: Monday,
    },

    MealDay2 {

    },

    ...
 }
"""


class MealPlan(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    expected_end_date = models.DateTimeField()
    actual_end_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for mealDay in self.mealDays:
            mealDay.save()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(expected_end_date__gte=models.F('creation_date')),
                name='expected_end_date_must_be_after_creation_date'
            )
        ]


class MealDay(models.Model):
    class WeekDays(models.TextChoices):
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

    mealPlan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='mealDays')
    weekDay = models.IntegerField(choices=WeekDays.choices)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for mealTime in self.mealTimes:
            mealTime.save()


class MealTime(models.Model):
    class MealTimes(models.TextChoices):
        BREAKFAST = "Breakfast"
        LUNCH = "Lunch"
        DINNER = "Dinner"
        SNACK = "Snack"

        @property
        def max(self):
            return max(len(item) for item in self)

    mealDay = models.ForeignKey(MealDay, on_delete=models.CASCADE, related_name='mealTimes')
    mealTime = models.CharField(choices=MealTimes.choices, max_length=MealTimes.max) # TODO potrebbe dare errori

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for meal in self.meals:
            meal.save()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mealDay', 'mealTime'], name='mealTime_must_be_unique_per_mealDay')
        ]


class Meal(models.Model):
    mealTime = models.ForeignKey(MealTime, on_delete=models.CASCADE, related_name='meals')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for ingredient in self.ingredients:
            ingredient.save()


class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    quantityType = models.CharField(max_length=30)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='ingredients')
