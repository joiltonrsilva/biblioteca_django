from django.urls import path
from . import views

urlpatterns = [
    path('cadastro-usuario/', views.CriarUsuario.as_view(), name='cadastro-usuario')
]
