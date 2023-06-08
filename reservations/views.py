import json
from datetime import date, timedelta

from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView, UpdateView

from reservations.forms import GymDayForm, ExceptionalGymDayForm
from reservations.models import Calendar, GymDay, ExceptionalGymDay, Reservation


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        print("Notifications workout: ", user.notifications.workout)
        context = super().get_context_data(**kwargs)
        # Parameter: date=2023-5
        if self.request.GET.get('date'):
            year, month = self.request.GET['date'].split('-')
            year, month = int(year), int(month)
        else:
            today = date.today()
            year, month = today.year, today.month

        context['next_month'] = f'{year}-{int(month) + 1}' if int(month) < 12 else f'{int(year) + 1}-1'
        context['prev_month'] = f'{year}-{int(month) - 1} ' if int(month) > 1 else f'{int(year) - 1}-12'
        context['calendar'] = Calendar.getCalendar(year, month)
        context['blank_days'] = '.' * int(context['calendar'].weeks[0].days[0].weekDay[0])
        return context


class EditGymDayView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    model = GymDay
    template_name = 'openinghourssettings.html'
    form_class = GymDayForm
    group_required = ['PersonalTrainer']
    context_object_name = 'openingHours'

    def get_success_url(self):
        return reverse_lazy('reservations')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        try:
            openingHours = GymDay.objects.get(dayOfWeek=pk)
        except GymDay.DoesNotExist:
            openingHours = GymDay(dayOfWeek=pk)
        return openingHours

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_context(**kwargs))
        return context

    def get_context(self, **kwargs):
        prev_day = self.object.dayOfWeek - 1 if self.object.dayOfWeek > 0 else 6
        next_day = self.object.dayOfWeek + 1 if self.object.dayOfWeek < 6 else 0
        prev_day_url = reverse_lazy('openinghours', kwargs={'pk': prev_day})
        next_day_url = reverse_lazy('openinghours', kwargs={'pk': next_day})
        context = {'day': self._day_to_string(self.object.dayOfWeek),
                   'prev_day_url': prev_day_url,
                   'next_day_url': next_day_url}

        return context

    @staticmethod
    def _day_to_string(day: int):
        if day == 0:
            return 'Lunedì'
        elif day == 1:
            return 'Martedì'
        elif day == 2:
            return 'Mercoledì'
        elif day == 3:
            return 'Giovedì'
        elif day == 4:
            return 'Venerdì'
        elif day == 5:
            return 'Sabato'
        elif day == 6:
            return 'Domenica'

    def form_valid(self, form):
        hours = form.cleaned_data['hours']
        old_hours = self.object.hours
        removed_hours = list(set(old_hours) - set(hours))
        for hour in removed_hours:
            Reservation.objects.filter(day__week_day=self.object.dayOfWeek, hour=hour).delete()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        Reservation.objects.filter(day__week_day=self.get_object().dayOfWeek).delete()
        return super().post(request, *args, **kwargs)


class EditExceptionalGymDayView(EditGymDayView):
    model = ExceptionalGymDay
    template_name = 'openinghourssettings.html'
    form_class = ExceptionalGymDayForm
    group_required = ['PersonalTrainer']

    def get_success_url(self):
        return reverse_lazy('reservations')

    def get_object(self, queryset=None):
        date_param = self.kwargs.get('date')
        day, month, year = date_param.split('-')
        my_date = date(year=int(year), month=int(month), day=int(day))
        try:
            exceptionalGymDay = ExceptionalGymDay.objects.get(date=my_date)
        except ExceptionalGymDay.DoesNotExist:
            exceptionalGymDay = ExceptionalGymDay(date=my_date)
            try:
                gymDay = GymDay.objects.get(dayOfWeek=my_date.weekday())
                exceptionalGymDay.hours = gymDay.hours
                exceptionalGymDay.capacity = gymDay.capacity
            except GymDay.DoesNotExist:
                pass

        return exceptionalGymDay

    def get_context(self, **kwargs):
        prev_day = self.object.date - timedelta(days=1)
        next_day = self.object.date + timedelta(days=1)
        prev_day_url = reverse_lazy('openinghours', kwargs={'date': prev_day.strftime('%d-%m-%Y')})
        next_day_url = reverse_lazy('openinghours', kwargs={'date': next_day.strftime('%d-%m-%Y')})
        context = {'day': f"{self._day_to_string(self.object.date.weekday())} {self.object.date.strftime('%d-%m-%Y')}",
                   'prev_day_url': prev_day_url,
                   'next_day_url': next_day_url}
        return context

    def form_valid(self, form):
        hours = form.cleaned_data['hours']
        old_hours = self.object.hours
        removed_hours = old_hours - hours
        year, month = self.object.date.year, self.object.date.month
        for hour in removed_hours:
            Calendar.getCalendar(year, month).getDay(self.object.date.day).deleteReservations(hour=hour)
        return super().form_valid(form)


@require_GET
@login_required
def get_day_info(request):
    year, month, day = int(request.GET['year']), int(request.GET['month']), int(request.GET['day'])
    calendarDay = Calendar.getCalendar(year, month).getDay(day)
    user = request.user

    data = {
        'openHours': calendarDay.openingHours,
        'fullHours': calendarDay.fullHours,
        'reservations': calendarDay.getReservations(user),
    }
    # Return the dictionary as a JSON response
    return JsonResponse(data)


@require_POST
@login_required
def make_reservation(
        request):
    try:
        body = json.loads(request.body)
        year, month, day, hour = body['year'], body['month'], body['day'], body['hour']
        user = request.user
        calendarDay = Calendar.getCalendar(year, month).getDay(day)
        calendarDay.makeReservation(hour, user)
    except Exception:
        return HttpResponse(status=400)
    return HttpResponse(status=201)


@require_POST
@login_required
def delete_reservation(request):
    try:
        body = json.loads(request.body)
        year, month, day, hour = body['year'], body['month'], body['day'], body['hour']
        user = request.user
        calendarDay = Calendar.getCalendar(year, month).getDay(day)
        calendarDay.deleteReservations(hour, user)
    except Exception:
        return HttpResponse(status=400)
    return HttpResponse(status=201)
