from django.shortcuts import render

from accounts.forms import UserRegistrationForm

__all__ = ('registration',)


def registration(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return render(request, 'accounts/done.html', {'user': user})
    return render(request, 'accounts/register.html', {'form': form})
