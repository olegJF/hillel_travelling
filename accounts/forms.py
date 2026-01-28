from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label="Введіть username", max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', })
    )
    password = forms.CharField(
        label="Введіть password", max_length=50, widget=forms.PasswordInput(
            attrs={'class': 'form-control', })
    )
    password1 = forms.CharField(
        label="Повторіть password", max_length=50, widget=forms.PasswordInput(
            attrs={'class': 'form-control', })
    )

    class Meta:
        model = User
        fields = ('username', )

    def clean_password1(self):
        data = self.cleaned_data
        if data['password'] != data['password1']:
            raise forms.ValidationError('Паролі не співпадають')
        return data['password1']

