from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.db import transaction
from django.urls import reverse_lazy
from .models import User, Profile
from .forms import UserProfileForm, EmailAuthenticationForm

# email: jeiel@gmail.com senha:12345678
# email: joilton@gmail.com senha:12345678

class Home(TemplateView):
    template_name = "home.html"
    

    def get_success_url(self):
        return self.request.GET.get('next','perfil')

class perfil(TemplateView):
    template_name = "perfil.html"
  
   

class Login(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'login.html'

    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        return response


class CreateUser(CreateView):
    model = Profile
    template_name = 'create_user.html'
    form_class = UserProfileForm
    success_url = reverse_lazy("login")

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    @transaction.atomic
    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        return response



