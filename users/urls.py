from django.urls import path,re_path
from . import views

urlpatterns = [
    path('cadastro-usuario/', views.CreateUser.as_view(), name='create-user'),
    path('home/', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('perfil/', views.perfil.as_view(), name='perfil'),
]
