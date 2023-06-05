from django.urls import path

from mealplans.views import UserMealPlanView, ManageMealPlansView, CreateMealPlanView, save_mealPlan, download_mealPlan, \
    EditMealPlanView

urlpatterns = [
    path('', UserMealPlanView.as_view(), name='meaplan'),
    path('manage/', ManageMealPlansView.as_view(), name='manage_mealplans'),
    path('manage/create/<str:userName>',CreateMealPlanView.as_view(), name='create_mealplan'),
    path('manage/saveMealPlan/<str:userName>', save_mealPlan, name='save_mealplan'),
    path('manage/edit/<str:userName>', EditMealPlanView.as_view(), name='edit_mealplan'),
    path('manage/downloadMealPlan/', download_mealPlan, name='download_mealPlan'),

]
