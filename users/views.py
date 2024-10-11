from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import User
from .forms import UserProfileForm


class Home(TemplateView):
    template_name = "home.html"


class CreateUser(CreateView):
    model = User
    template_name='create_user.html'
    form_class = UserProfileForm
    sucess_url = reverse_lazy("home")


class ListUser(ListView):
    model = User
    template_name = 'list_users.html'
    context_object_name = 'usuarios'
    ordering = ['-id']


class EditUser(UpdateView):
    model = User
    template_name = 'edit_user.html'
    form_class = UserProfileForm
    sucess_url = reverse_lazy("home")
