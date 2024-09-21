from django.db import models

# Create your models here.
class Cadastro(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField('exemple@gmail.com')
    senha = models.CharField(max_length=8)

    def __str__(self):
        return self.nome
    