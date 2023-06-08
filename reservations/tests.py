import datetime
from typing import List

from django.test import TestCase

from GymApp.models import GymUser
from reservations.models import Reservation, Calendar, Day, GymDay, ExceptionalGymDay


class CalendarTest(TestCase):


    def make_reservation_function(self):
        calendar: Calendar = Calendar.getCalendar(2023, 6)
        day: Day = calendar.getDay(24)
        day.makeReservation(10, GymUser.objects.get(username='testuser30'))
    def test_if_full_check_works(self):
        calendar: Calendar = Calendar.getCalendar(2023, 6)
        day: Day = calendar.getDay(24)
        self.create_gym_day(day.weekDay[0], 30, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        self.make_reservations(day.date, hour=10, number_of_reservations=30)
        self.assertRaises(ValueError, self.make_reservation_function)

    def test_if_full_check_works_when_not_full(self):
        calendar: Calendar = Calendar.getCalendar(2023, 6)
        day: Day = calendar.getDay(24)
        self.create_gym_day(day.weekDay[0], 30, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        self.make_reservations(day.date, hour=10, number_of_reservations=29)
        try:
            self.make_reservation_function()
        except ValueError:
            self.fail("makeReservation() raised ValueError unexpectedly!")

    def test_if_full_check_works_with_exceptional_day(self):
        calendar: Calendar = Calendar.getCalendar(2023, 6)
        day: Day = calendar.getDay(24)
        self.create_exceptional_gym_day(day.date, 30, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        self.make_reservations(day.date, hour=10, number_of_reservations=30)
        self.assertRaises(ValueError, self.make_reservation_function)

    def test_if_full_check_works_with_exceptional_day_when_not_full(self):
        calendar: Calendar = Calendar.getCalendar(2023, 6)
        day: Day = calendar.getDay(24)
        self.create_exceptional_gym_day(day.date, 30, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        self.make_reservations(day.date, hour=10, number_of_reservations=29)
        try:
            self.make_reservation_function()
        except ValueError:
            self.fail("makeReservation() raised ValueError unexpectedly!")

    def create_exceptional_gym_day(self, date: datetime.date, capacity: int, hours: List[int]):
        ExceptionalGymDay.objects.create(
            date=date,
            capacity=capacity,
            hours=hours
        )

    def create_gym_day(self, dayOfWeek: int, capacity: int, hours: List[int]):
        GymDay.objects.create(
            dayOfWeek=dayOfWeek,
            capacity=capacity,
            hours=hours
        )

    # Methods to startup e release

    def make_reservations(self, day: datetime.date, hour, number_of_reservations: int):
        for i in range(number_of_reservations):
            Reservation.objects.create(
                user=GymUser.objects.get(username=f'testuser{i}'),
                day=day,
                hour=hour
            )

    def create_gymusers(self):
        for i in range(31):
            GymUser.objects.create_user(
                username=f'testuser{i}',
                password='12345'
            )

    def setUp(self):
        self.create_gymusers()

    def tearDown(self):
        GymUser.objects.all().delete()
        Reservation.objects.all().delete()
        GymDay.objects.all().delete()
        ExceptionalGymDay.objects.all().delete()
