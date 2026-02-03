from django import forms
from .models import Subscription
from django.utils import timezone


class SubscriptionCreateForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            'name',
            'price',
            'currency',
            'period',
            'next_payment_date',
            'is_active',
            'service_url',
            'note',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Spotify Premium и т.д.'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'period': forms.Select(attrs={'class': 'form-select'}),
            'next_payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'service_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Дополнительные заметки...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].initial = True
        self.fields['next_payment_date'].initial = timezone.now().date()