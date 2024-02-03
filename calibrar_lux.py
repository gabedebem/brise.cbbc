#!/usr/bin/python3

import csv
from pathlib import Path
from datetime import datetime
import time

from lux import ler_lux

file = 'leitura_lux.csv'

if __name__ == "__main__":
    while True:
        exists = Path(file).is_file()
        lux = ler_lux()
        with open(file, 'a', newline='') as f:
            fieldnames = ['Data/Hora', 'e_table', 'e_eye']
            escrever = csv.DictWriter(f, fieldnames=fieldnames)
            if not exists:
                escrever.writeheader()
            lux['Data/Hora'] = datetime.now() 
            escrever.writerow(lux)
            print(lux)
        time.sleep(60)