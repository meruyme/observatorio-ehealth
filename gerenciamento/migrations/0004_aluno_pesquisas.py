# Generated by Django 3.2.3 on 2022-05-01 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa', '0001_initial'),
        ('gerenciamento', '0003_hospital_pais'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='pesquisas',
            field=models.ManyToManyField(through='pesquisa.AlunoPesquisa', to='pesquisa.Pesquisa'),
        ),
    ]
