# forms.py
from django import forms

from bullettinboard.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'maxlength': 512, 'placeholder': 'Scrivi il tuo messaggio...',
                                          'class': 'form-control'})
        }
