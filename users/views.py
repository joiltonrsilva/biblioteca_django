from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.db import transaction
from django.urls import reverse_lazy
from .models import User, Profile
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm, EmailAuthenticationForm

# email: jeiel@gmail.com senha:12345678
# email: joilton@gmail.com senha:12345678

class HomeView(TemplateView):
    template_name = "home.html"
    
    # def get_success_url(self):
    #     return self.request.GET.get('next','perfil')


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = "perfil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
  
   

class LoginViews(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'login.html'

    redirect_authenticated_user = True

    def form_valid(self, form):
        print("VALID")
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        print("INVALID")
        response = self.render_to_response(self.get_context_data(form=form))
        return response


class CreateUserView(CreateView):
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



