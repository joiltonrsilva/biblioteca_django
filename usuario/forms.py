from django import forms

from .models import Usuario


class UsuarioForm(forms.ModelForm):
    username = forms.CharField(label="Usuário")
    senha1 = forms.CharField(label='Senha 1', widget=forms.PasswordInput)
    senha2 = forms.CharField(label='Senha 2', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ("email", "username")

    def clean_senha(self):
        senha_1 = self.cleaned_data.get("senha_1")
        senha_2 = self.cleaned_data.get("senha_2")

        if senha_1 and senha_2 and senha_1 != senha_2:
            raise forms.ValidationError("As senhas informadas não são iguais.")
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["senha_1"])
        if commit:
            usuario.save()
        return usuario