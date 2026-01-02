from django import forms

from cities.models import City


class HtmlForm(forms.Form):
    name = forms.CharField(label="Місто", max_length=100)


class CityForm(forms.ModelForm):
    name = forms.CharField(
        label="Місто", max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Назва міста'})
    )

    class Meta:
        model = City
        fields = ('name',)
