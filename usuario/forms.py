from django import forms
from django.core.validators import RegexValidator
from .models import Usuario, Profile
import re

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(label="Usuário", required=True)
    email = forms.EmailField(label="Email", validators=[RegexValidator(regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z.]+$', message='Digite um endereço de email válido.')],required=True)
    senha1 = forms.CharField(label='Senha', widget=forms.PasswordInput, validators=[RegexValidator(regex=r'^[a-zA-Z0-9]+$', message="A senha deve conter apenas letras e números.")],required=True)
    senha2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    print(username, email, senha1, senha2)

  
    class Meta:
        model = Usuario
        fields = ("email",)
    
    def clean_senha(self):
        cleaned_data = super().clean()
        senha_1 = self.cleaned_data.get("senha_1")
        senha_2 = self.cleaned_data.get("senha_2")
     
       
        if senha_1 != senha_2:
            raise forms.ValidationError("As senhas não coincidem.")
        else:
            raise forms.ValidationError("as senhas coincidem.")
        return cleaned_data


    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["senha_1"])
        if commit:
            usuario.save()
        print(usuario)
        return usuario


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'birthday']

# class UsuarioProfileForm(forms.Form):
#     usuario_form = UsuarioForm()
#     Profile_form = ProfileForm()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields.update(self.usuario_form.fields)
#         self.fields.update(self.porfile_form.fields)

#     def save(self, commit=True):
#         # Salvando o usuário
#         usuario_form = UsuarioForm(self.data)
#         user = usuario_form.save(commit=False)
#         if commit:
#             user.save()

#         # Salvando o perfil associado ao usuário
#         porfile_form = ProfileForm(self.data)
#         profile = porfile_form.save(commit=False)
#         profile.user = user
#         if commit:
#             profile.save()

#         return user