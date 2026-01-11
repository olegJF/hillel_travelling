from django import forms

from cities.models import City
from trains.models import Train


class TrainForm(forms.ModelForm):
    number = forms.CharField(
        label="Потяг", max_length=10, widget=forms.TextInput(
            attrs={'class': 'form-control', })
    )
    travel_time = forms.DecimalField(
        label='Час у дорозі', widget=forms.NumberInput(
            attrs={'class': 'form-control', }
        ))
    from_city = forms.ModelChoiceField(
        label='З якого міста', queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', })
    )
    to_city = forms.ModelChoiceField(
        label='До якого міста', queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', })
    )

    class Meta:
        model = Train
        fields = '__all__'
