from django.urls import path,re_path
from . import views

urlpatterns = [
    path('cadastro-usuario/', views.CreateUser.as_view(), name='cadastro-usuario'),
    path('list/', views.ListUser.as_view(), name='list_users'),
    path('edit/<int:pk>/', views.EditUser.as_view(), name='edit_user'),
    path('home/', views.Home.as_view(), name='home'),
]
