# Generated by Django 3.2.3 on 2022-05-15 00:54

from django.db import migrations, models
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0007_auto_20220514_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='cpf',
            field=localflavor.br.models.BRCPFField(max_length=14, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='matricula',
            field=models.CharField(max_length=13, verbose_name='Matrícula'),
        ),
        migrations.AlterField(
            model_name='coordenador',
            name='cpf',
            field=localflavor.br.models.BRCPFField(max_length=14, verbose_name='CPF'),
        ),
    ]