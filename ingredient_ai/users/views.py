from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .services import add_to_wishlist, delete_from_wishlist, get_wishlist


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


def add_to_wishlist_view(request, pk):
    add_to_wishlist(request.user.id, pk)

    return redirect(request.GET.get('next', '/'))


def delete_from_wishlist_view(request, pk):
    delete_from_wishlist(request.user.id, pk)

    return redirect(request.GET.get('next', '/'))


def get_wishlist_view(request):
    wishlist_recipes = get_wishlist(request.user.id)
    context = {'wishlist_recipes': wishlist_recipes}

    return render(request, 'users/wishlist.html', context)
