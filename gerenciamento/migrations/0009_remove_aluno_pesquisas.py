# Generated by Django 3.2.3 on 2022-05-15 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0008_auto_20220514_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='pesquisas',
        ),
    ]
