import json
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView, UpdateView

from reservations.forms import GymDay, GymDayForm, ExceptionalGymDayForm
from reservations.models import Calendar, GymDay, ExceptionalGymDay


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


class EditGymDayView(LoginRequiredMixin, UpdateView):
    model = GymDay
    template_name = 'openinghourssettings.html'
    form_class = GymDayForm

    def get_success_url(self):
        return reverse_lazy('reservations')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')  # 'pk' è il nome del parametro nell'URL
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
                   'next_day_url': next_day_url
                   }

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


class EditExceptionalGymDayView(EditGymDayView):
    model = ExceptionalGymDay
    template_name = 'openinghourssettings.html'
    form_class = ExceptionalGymDayForm

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
        request):  # TODO fai controlli di ogni tipo ( come quando si modificano le ore di apertura, eliminare le riservazioni che non sono più possibili)
    # TODO inoltre controlla se il JSOn è giusto
    body = json.loads(request.body)
    year, month, day, hour = body['year'], body['month'], body['day'], body['hour']
    user = request.user

    calendarDay = Calendar.getCalendar(year, month).getDay(day)
    try:
        calendarDay.makeReservation(hour, user)
    except Exception:
        return HttpResponse(status=400)
    return HttpResponse(status=201)


@require_POST
@login_required
def delete_reservation(request):
    body = json.loads(request.body)
    year, month, day, hour = body['year'], body['month'], body['day'], body['hour']
    user = request.user

    calendarDay = Calendar.getCalendar(year, month).getDay(day)
    try:
        calendarDay.deleteReservation(hour, user)
    except Exception:
        return HttpResponse(status=400)
    return HttpResponse(status=201)
