import calendar
from dataclasses import dataclass
from datetime import date
from itertools import groupby
from typing import List

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from GymApp.models import GymUser
from GymApp.utils import WeekDay
from reservations.fields import IntegerListField


class GymDay(models.Model):
    dayOfWeek = models.IntegerField(primary_key=True, choices=WeekDay.choices)
    hours = IntegerListField()
    capacity = models.IntegerField(default=30)


class ExceptionalGymDay(models.Model):
    date = models.DateField(primary_key=True)
    hours = IntegerListField()
    capacity = models.IntegerField(default=30)


class Reservation(models.Model):
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    day = models.DateField()
    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])

    class Meta:
        unique_together = [['user', 'day', 'hour']]


@dataclass
class Day:
    weekDay: WeekDay
    date: date

    @property
    def capacity(self):
        exceptionalGymDay = ExceptionalGymDay.objects.filter(date=self.date).first()
        if exceptionalGymDay:
            return exceptionalGymDay.capacity
        gymDay = GymDay.objects.filter(dayOfWeek=self.weekDay[0]).first()
        if gymDay:
            return gymDay.capacity
        return 0

    @property
    def isClosed(self):
        return not GymDay.objects.filter(dayOfWeek=self.weekDay[0]).exists()

    @property
    def openingHours(self) -> List[int]:
        exceptionalGymDay = ExceptionalGymDay.objects.filter(date=self.date).first()
        if exceptionalGymDay:
            return exceptionalGymDay.hours
        gymDay = GymDay.objects.filter(dayOfWeek=self.weekDay[0]).first()
        if gymDay:
            return gymDay.hours
        return []

    @property
    def fullHours(self) -> List[int]:
        reservations = Reservation.objects.filter(day=self.date)
        grouped = groupby(reservations, key=lambda x: x.hour)
        return [hour for hour, group in grouped if len(list(group)) >= self.capacity]

    def makeReservation(self, hour, user):
        if hour in self.fullHours:
            raise ValueError(f"Hour {hour} is full")
        if hour not in self.openingHours:
            raise ValueError(f"Hour {hour} is not open")
        Reservation.objects.create(user=user, day=self.date, hour=hour)

    def getReservations(self, user=None):
        try:
            if user is None:
                return [reservation.hour for reservation in Reservation.objects.filter(day=self.date)]
            return [reservation.hour for reservation in Reservation.objects.filter(day=self.date, user=user)]
        except Reservation.DoesNotExist:
            return []

    def deleteReservations(self, hour=None, user=None):
        if user is None:
            if hour is None:
                Reservation.objects.filter(day=self.date).delete()
            else:
                Reservation.objects.filter(day=self.date, hour=hour).delete()
        else:
            if hour is None:
                Reservation.objects.filter(day=self.date, user=user).delete()
            else:
                Reservation.objects.filter(day=self.date, hour=hour, user=user).delete()


@dataclass
class Week:
    days: List[Day]

    def __iter__(self):
        return iter(self.days)

    def __len__(self):
        return len(self.days)


@dataclass
class Calendar:
    year: int
    month: int
    weeks: List[Week]
    month_names = {
        1: "gennaio",
        2: "febbraio",
        3: "marzo",
        4: "aprile",
        5: "maggio",
        6: "giugno",
        7: "luglio",
        8: "agosto",
        9: "settembre",
        10: "ottobre",
        11: "novembre",
        12: "dicembre",
    }

    @property
    def literalMonth(self):
        return self.month_names[self.month]

    @staticmethod
    def getCalendar(year: int, month: int) -> 'Calendar':
        _, last_day = calendar.monthrange(year, month)
        weeks = []

        start_day = 1
        while start_day <= last_day:
            days = []
            if start_day == 1:
                for weekday in range(int(WeekDay.fromDate(date(year, month, start_day))[0]), 7):
                    days.append(Day(date=date(year, month, start_day),
                                    weekDay=WeekDay.fromDate(date(year, month, start_day))))
                    start_day += 1
                week = Week(days)
                weeks.append(week)
                continue
            for weekday in range(7):
                if start_day > last_day:
                    break
                day = Day(date=date(year, month, start_day), weekDay=WeekDay.fromDate(date(year, month, start_day)))
                days.append(day)
                start_day += 1
            week = Week(days)
            weeks.append(week)

        return Calendar(year, month, weeks)

    def __str__(self):
        return self.__dict__.__str__()

    def getDay(self, day) -> Day:
        for week in self.weeks:
            for d in week.days:
                if d.date.day == day:
                    return d
        raise ValueError(f"Day {day} not found")
