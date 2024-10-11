from django import forms
from django.core.validators import RegexValidator
from .models import User, Profile
import re

class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(label="Email", validators=[RegexValidator(regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z.]+$', message='Digite um endereço de email válido.')],required=True)
    password_1 = forms.CharField(label='Senha', widget=forms.PasswordInput, validators=[RegexValidator(regex=r'^[a-zA-Z0-9]+$', message="A senha deve conter apenas letras e números.")],required=True)
    password_2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password_1", "password_2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def clean_password1(self):
        cleaned_data = super().clean()
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")

        if password_1 != password_2:
            raise forms.ValidationError("As senhas não coincidem.")
        else:
            raise forms.ValidationError("as senhas coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'birthday']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Captura a instância do usuário, se existir
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # Instancia o CreateUserForm e o ProfileForm com os dados de instance, se houver
        self.user_form = CreateUserForm(*args, instance=instance, **kwargs)
        self.profile_form = ProfileForm(*args, instance=instance.profile if instance else None, **kwargs)

        # Atualiza os campos do UserProfileForm com os campos de ambos os formulários
        self.fields.update(self.user_form.fields)
        self.fields.update(self.profile_form.fields)

    def is_valid(self):
        # Verifica se ambos os formulários são válidos
        return self.user_form.is_valid() and self.profile_form.is_valid()

    def save(self, commit=True):
        # Salva os dados do CreateUserForm (usuário)
        user = self.user_form.save(commit=False)
        
        # Salva os dados do ProfileForm (perfil) e associa ao usuário
        profile = self.profile_form.save(commit=False)
        profile.user = user

        if commit:
            user.save()
            profile.save()

        return user
