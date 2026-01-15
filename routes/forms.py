from django import forms

from cities.models import City
from trains.models import Train


class RouteForm(forms.Form):
    expected_time = forms.DecimalField(
        label='Час у дорозі', widget=forms.NumberInput(
            attrs={'class': 'form-control', }
        ))
    from_city = forms.ModelChoiceField(
        label='З якого міста', queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control basic-single', })
    )
    to_city = forms.ModelChoiceField(
        label='До якого міста', queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control basic-single', })
    )
    cities = forms.ModelMultipleChoiceField(
        label='Через міста', queryset=City.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control basic-multiple', })
    )
