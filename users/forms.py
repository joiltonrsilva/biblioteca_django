from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import User, Profile

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email", 
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9.+_-]+@[a-zA-Z.]+$', message='Digite um endereço de email válido.')],
        required=True
    )
    password_1 = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput, 
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9]+$', message="A senha deve conter apenas letras e números.")],
        required=True
    )
    password_2 = forms.CharField(
        label='Confirme a senha', 
        widget=forms.PasswordInput, 
        required=True
    )

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está cadastrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")

        if password_1 and password_2 and password_1 != password_2:
            self.add_error('password_2', "As senhas não coincidem.")
            raise forms.ValidationError("As senhas não coincidem.")

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Captura a instância do usuário, se existir
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # Instancia o UserForm e o ProfileForm com os dados de instance, se houver
        self.user_form = UserForm(*args, instance=instance, **kwargs)
        self.profile_form = ProfileForm(*args, instance=instance.profile if instance else None, **kwargs)

        # Atualiza os campos do UserProfileForm com os campos de ambos os formulários
        self.fields.update(self.user_form.fields)
        self.fields.update(self.profile_form.fields)

    def is_valid(self):
        # Verifica se ambos os formulários são válidos
        return self.user_form.is_valid() and self.profile_form.is_valid()

    def save(self, commit=True):
        # Salva os dados do UserForm (usuário)
        user = self.user_form.save(commit=False)
        
        # Salva os dados do ProfileForm (perfil) e associa ao usuário
        profile = self.profile_form.save(commit=False)
        profile.user = user

        if commit:
            user.save()
            profile.save()

        return user