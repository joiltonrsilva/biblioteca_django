from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from .user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email
    as a unique identifier.
    """
    email: models.EmailField = models.EmailField(
        verbose_name=_("Email"),
        max_length=100,
        unique=True
    )
    is_admin: models.BooleanField = models.BooleanField(
        verbose_name=_("Admin Status"),
        default=False,
    )
    date_joined: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Join Date"),
        auto_now_add=True,
    )
    last_modified: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Last Modified"),
        auto_now=True,
    )
    is_active = models.BooleanField("Ativo", default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    """
    Profile model for users.
    """
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=60,
    )
    birthday = models.DateField(
        verbose_name=_("Birthday"),
    )
    user = models.OneToOneField(
        to="users.User",
        verbose_name=_("User"),
        on_delete=models.RESTRICT,
        related_name="profile_user_user",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
