from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from GymApp.models import GymUser
from mealplans.models import MealPlan, MealDay, Meal, Ingredient


class UserMealPlanViewTest(TestCase):
    client = Client()

    def test_if_mealplan_is_missing(self):
        response = self.client.get(reverse('meaplan'), user='testuser')
        self.assertContains(response, 'Nessuna dieta disponibile', status_code=200)

    def test_if_mealplan_is_present(self):
        self.create_gym_user_meal_plan()
        response = self.client.get(reverse('meaplan'), user='testuser')
        self.assertNotContains(response, 'Nessuna dieta disponibile', status_code=200)

    def create_gym_user_meal_plan(self):
        mealPlan = MealPlan.objects.create(
            expected_end_date=datetime.now() + timedelta(days=7),
            user=GymUser.objects.get(username='testuser')
        )

        for i in range(1, 5):
            mealDay = MealDay.objects.create(
                day=i,
                mealPlan=mealPlan
            )
            for j in range(1, 4):
                meal = Meal.objects.create(
                    name=f'meal{j}',
                    mealDay=mealDay
                )
                for k in range(1, 4):
                    Ingredient.objects.create(
                        name=f'ingredient{k}',
                        quantity=k,
                        quantityType='g',
                        meal=meal
                    )

    def create_gym_user(self):
        return GymUser.objects.create(
            username='testuser',
            password='testpassword',
        )

    def setUp(self) -> None:
        user = self.create_gym_user()
        self.client.force_login(user)

    def tearDown(self) -> None:
        GymUser.objects.all().delete()
        MealPlan.objects.all().delete()
