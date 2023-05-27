from django.urls import path, re_path

from reservations.views import CalendarView, get_day_info, EditGymDayView, EditExceptionalGymDayView, make_reservation, \
    delete_reservation

urlpatterns = [
    path('', CalendarView.as_view(), name='reservations'),
    path('<int:pk>/openinghours', EditGymDayView.as_view(), name='openinghours'),
    path('dayinfo/', get_day_info, name='day-info'),
    path('makereservation/',make_reservation, name='make-reservation'),
    path('deletereservation/',delete_reservation, name='delete-reservation'),
    re_path(r'^(?P<date>\d{1,2}-\d{1,2}-\d{4})/openinghours', EditExceptionalGymDayView.as_view(), name='openinghours'),
]
