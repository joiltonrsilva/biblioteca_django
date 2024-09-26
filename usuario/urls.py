from django.urls import path
from . import views

urlpatterns = [
    path('cadastro-usuario/', views.cadastro, name='cadastro-usuario')
]
