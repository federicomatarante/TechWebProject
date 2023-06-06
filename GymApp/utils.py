from django.db import models
from io import BytesIO
from datetime import date
import pdfkit
from django.http import FileResponse


def get_or_error(dictionary, key, type):
    value = dictionary.get(key)
    if not value:
        raise ValueError(f'{key} is required')
    if not isinstance(value, type):
        raise ValueError(f'{key} must be of type {type}')
    return value


def send_pdf(html_content, file_name):
    pdf_data = pdfkit.from_string(html_content, False)
    buffer = BytesIO(pdf_data)
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
    return response


class WeekDay(models.TextChoices):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @staticmethod
    def fromDate(date: date) -> 'WeekDay':
        weekDay = date.weekday()
        return WeekDay.choices[weekDay]


def isPersonalTrainer(user):
    return user.is_authenticated and ('PersonalTrainer' in user.groups.values_list('name', flat=True) or user.is_superuser)
