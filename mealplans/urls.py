from django.urls import path

from mealplans.views import UserMealPlanView

urlpatterns = [
    path('', UserMealPlanView.as_view(), name='workout'),
]
