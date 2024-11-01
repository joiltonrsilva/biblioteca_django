from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('cadastro-usuario/', views.CreateUserView.as_view(), name='create-user'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginViews.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
]
