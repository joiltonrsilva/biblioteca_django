from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.urls import reverse_lazy
from .models import User, Profile
from .forms import UserProfileForm, EmailAuthenticationForm


class Home(TemplateView):
    template_name = "home.html"


class Login(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return self.request.GET.get('next', 'home')


class CreateUser(CreateView):
    model = Profile
    template_name = 'create_user.html'
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    @transaction.atomic
    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        return response


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
