from django import forms

from cities.models import City
from routes.models import Route
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


class RouteModelForm(forms.ModelForm):
    name = forms.CharField(
        label='Назва маршруту', widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Назва маршруту'}
        ))
    total_time = forms.DurationField(widget=forms.HiddenInput())
    from_city = forms.ModelChoiceField(
        queryset=City.objects.all(), widget=forms.HiddenInput()
    )
    to_city = forms.ModelChoiceField(
        queryset=City.objects.all(), widget=forms.HiddenInput()
    )
    trains = forms.ModelMultipleChoiceField(
        queryset=Train.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control d-none', })
    )

    class Meta:
        model = Route
        fields = ('name', 'total_time', 'from_city', 'to_city', 'trains')
