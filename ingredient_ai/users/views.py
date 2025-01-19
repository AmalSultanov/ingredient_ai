from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .utils import add_to_wishlist, delete_from_wishlist, get_wishlist


class CustomLoginView(LoginView):
    template_name = 'users/registration/login.html'


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('/')

    form = RegistrationForm()
    context = {'form': form}

    return render(request, 'users/registration/registration.html', context)
