from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm
from .services import add_to_wishlist, delete_from_wishlist, get_wishlist


class CustomLoginView(LoginView):
    template_name = 'users/registration/login.html'


class RegistrationCreateView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/registration/registration.html'
    success_url = reverse_lazy('recipes:ingredients')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect(self.success_url)


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
