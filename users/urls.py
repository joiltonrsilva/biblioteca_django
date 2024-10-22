from django.urls import path,re_path
from . import views

urlpatterns = [
    path('cadastro-usuario/', views.CreateUser.as_view(), name='create-user'),
    path('list/', views.ListUser.as_view(), name='list-users'),
    path('edit/<int:pk>/', views.EditUser.as_view(), name='edit-user'),
    path('home/', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
]
