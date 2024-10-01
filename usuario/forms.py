from django import forms
from django.core.validators import RegexValidator
from .models import Usuario
import re

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(label="Usuário", required=True)
    email = forms.EmailField(label="Email", validators=[RegexValidator(regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z.]+$', message='Digite um endereço de email válido.')],required=True)
    senha1 = forms.CharField(label='Senha', widget=forms.PasswordInput, validators=[RegexValidator(regex=r'^[a-zA-Z0-9]+$', message="A senha deve conter apenas letras e números.")],required=True)
    senha2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    print(username, email, senha1, senha2)

  
    class Meta:
        model = Usuario
        fields = ("email", "username")
    
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