from django.urls import path,re_path
from . import views

urlpatterns = [
    path('cadastro-usuario/', views.CriarUsuario.as_view(), name='cadastro-usuario'),
    #re_path(r^/(?Pusername\w+)/$),views.perfil
]
