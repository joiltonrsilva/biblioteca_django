# Generated by Django 5.1.1 on 2024-09-21 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cadastro',
            new_name='Usuario',
        ),
    ]