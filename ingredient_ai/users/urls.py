from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.registration_view, name='register'),
    path('logout', views.logout_view, name='logout'),
]
