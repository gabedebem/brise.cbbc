#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import os

from sensores_temperatura import ler_temperaturas

### Temperaturas
# data = datetime.now().strftime('%Y-%m-%d')
# nome_arquivo = f'sensores/todos_sensores-{data}.csv'
caminho = os.path.dirname(os.path.realpath(__file__))
nome_arquivo = 'leitura_temps.csv'
arquivo = os.path.join(caminho, nome_arquivo)
file_exists = os.path.isfile(arquivo)

with open(arquivo, mode='a') as arquivo:
    temperaturas = ler_temperaturas()
    temperaturas['Data Hora'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    writer = csv.DictWriter(arquivo, delimiter=',', quotechar='"', lineterminator='\n', fieldnames=temperaturas.keys())

    if not file_exists:
        writer.writeheader()

    writer.writerow(temperaturas)
