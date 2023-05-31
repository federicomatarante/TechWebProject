from django.urls import path, re_path

from workout.exercise_views import ExerciseListView, ExerciseCreateView, ExerciseUpdateView, delete_exercise
from workout.views import UserWorkoutPlanView, ManageWorkoutsView, CreateWorkoutView, save_workout, UpdateWorkoutView, \
    download_workout

urlpatterns = [
    path('', UserWorkoutPlanView.as_view(), name='workout'),
    path('manage/', ManageWorkoutsView.as_view(), name='manage_workouts'),
    path('manage/exercises', ExerciseListView.as_view(), name='exercise_list'),
    path('manage/exercises/<int:pk>/', ExerciseUpdateView.as_view(), name='update_exercise'),
    path('manage/createexercise', ExerciseCreateView.as_view(), name='create_exercise'),
    path('manage/deleteexercise/<int:pk>/', delete_exercise, name='delete_exercise'),
    path('manage/createWorkout/<str:userName>', CreateWorkoutView.as_view(), name='user_workout'),
    path('manage/updateWorkout/<str:userName>', UpdateWorkoutView.as_view(), name='update_workout_view'),
    path('manage/saveWorkout/<str:userName>', save_workout, name='save_workout'),
    path('manage/downloadWorkout/', download_workout, name='download_workout'),
]

