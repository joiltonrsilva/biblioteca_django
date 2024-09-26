from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Usuario

from .forms import UsuarioForm

class CriarUsuario(CreateView):
    model = Usuario
    template_name='cadastro_usuario.html'
    form_class = UsuarioForm
    sucess_url = reverse_lazy("home")