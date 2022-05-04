from django.core.management.base import BaseCommand
from gerenciamento.models import Pais
import pandas as pd
import os


class Command(BaseCommand):
    help = 'Importa arquivo csv com países e siglas'

    def handle(self, *args, **options):
        try:
            df_paises = pd.read_csv(os.path.join('gerenciamento', 'management', 'paises.csv', ), keep_default_na=False,
                                    encoding='utf-8')
            df_paises.apply(lambda x: Pais.objects.get_or_create(nome=x['value'], sigla=x['id']), axis=1)
            print("Países importados com sucesso!")
        except Exception as e:
            print(e)
