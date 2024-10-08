from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

# Create your models here.
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('exemple@gmail.com', unique=True)
    senha = models.CharField(max_length=8)
    is_admin: models.BooleanField = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField("Ativo", default=True)

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin

class Profile(models.Model):
    name = models.CharField(
        max_length=60,
    )
    birthday = models.DateField(
        name="Data de Nascimento"
    )
    user = models.OneToOneField(
        to="usuario.Profile",
        on_delete=models.RESTRICT,
        related_name="profile_user_user",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
