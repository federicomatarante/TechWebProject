from django import forms
from django.forms import Widget, RadioSelect

from reservations.models import GymDay, ExceptionalGymDay


class GymDayForm(forms.ModelForm):
    hours = forms.MultipleChoiceField(
        choices=[(i, str(i)) for i in range(0, 24)],
        widget=forms.CheckboxSelectMultiple(attrs={'style': 'display: inline-block; margin-right: 10px;'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hours'].initial = self.instance.hours
        self.fields['capacity'].initial = self.instance.capacity

    class Meta:
        model = GymDay
        fields = ["hours", 'capacity']

    def clean(self):
        cleaned_data = super().clean()
        if 'hours' in cleaned_data:
            cleaned_data['hours'] = [int(hour) for hour in cleaned_data['hours']]
        return cleaned_data

    def save(self, commit=True):
        return self.instance.save()


class ExceptionalGymDayForm(GymDayForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ExceptionalGymDay
        fields = ["hours", 'capacity']
