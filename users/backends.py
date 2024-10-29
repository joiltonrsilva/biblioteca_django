from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = get_object_or_404(user_model, email=username)
        except Http404:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
