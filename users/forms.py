from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User, Profile
   
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    email = forms.EmailField(label="Email",validators=[EmailValidator(message='Digite um endereço de e-mail válido.')],required=True)
    password_1 = forms.CharField(label='Senha', widget=forms.PasswordInput,validators=[RegexValidator( regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
            message="A senha deve conter pelo menos 8 caracteres, incluindo uma letra, um número e um caractere especial." )],
        required=True
    )
    password_2 = forms.CharField( label='Confirme a senha',widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")

        if password_1 and password_2 and password_1 != password_2:
            self.add_error('password_2', "As senhas não coincidem.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_1"])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    
    birthday = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Profile
        fields = ['name', 'birthday']

class UserProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        self.user_form = UserForm(*args, instance=instance, **kwargs)
        self.profile_form = ProfileForm(*args, instance=instance.profile if instance else None, **kwargs)

        self.fields.update(self.user_form.fields)
        self.fields.update(self.profile_form.fields)

    def is_valid(self):
        is_user_valid = self.user_form.is_valid()
        is_profile_valid = self.profile_form.is_valid()

        if not is_user_valid:
            for field, error in self.user_form.errors.items():
                self.add_error(field, error)
        if not is_profile_valid:
            for field, error in self.profile_form.errors.items():
                self.add_error(field, error)

        return is_user_valid and is_profile_valid

    def save(self, commit=True):
        user = self.user_form.save(commit=False)
        profile = self.profile_form.save(commit=False)
        profile.user = user

        if commit:
            user.save()
            profile.save()

        return user



class EmailAuthenticationForm(forms.Form):
    """
    Formulário de autenticação usando email como nome de usuário.
    """

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(email)s and password. Note that both "
            "are case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.fields["email"].label},
        )

    def confirm_login_allowed(self, user):
        """
        Verifica se o usuário pode fazer login.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"], code="inactive"
            )
