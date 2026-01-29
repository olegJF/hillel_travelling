from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()

__all__ = ('UserLoginForm', 'UserRegistrationForm')


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


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Введіть username", max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', })
    )
    password = forms.CharField(
        label="Введіть password", max_length=50, widget=forms.PasswordInput(
            attrs={'class': 'form-control', })
    )

    def clean(self):
        data = self.cleaned_data
        username = data.get('username')
        password = data.get('password')
        if password and username:
            user = User.objects.filter(username=username).first()
            if not user:
                raise forms.ValidationError('Такого користувача немає')
            if not check_password(password, user.password):
                raise forms.ValidationError('Невірний пароль')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Цей користувач не є активним')
        return super().clean()

