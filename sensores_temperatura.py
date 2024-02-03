import os
from logs.config import *

sensores = {
    '28-d9a50d1e64ff': 'tin',
    '28-d9c00d1e64ff': 'tg',
    '28-adeb0d1e64ff': 'tout',
    '28-16dc0d1e64ff': 'tfoot',
    '28-37c50d1e64ff': 'tabd',
}

# Configuracoes dos diretorios W1
base_dir = '/sys/bus/w1/devices/'
# device_folders = os.listdir(base_dir)


def read_temp_raw(device_file):
    try:
        f = open(os.path.join(base_dir, device_file), 'r')
        line = f.readlines()[-1]  # ultima linha somente
        f.close()
    except FileNotFoundError as fnf:
        log.error(f'Sensor não encontrado - {device_file}')
        log.exception(fnf)
        return 0
    except Exception as e:
        log.error(f'Erro ao ler sensor - {device_file}')
        log.exception(e)
        return 0
    return line


def read_temp(folder):
    line = read_temp_raw(os.path.join(folder, 'w1_slave'))
    if not(line):
        log.error(f'Erro ao ler temperatura no folder - {folder}')
        return 0
    equals_pos = line.find('t=')
    if equals_pos != -1:
        temp_string = line[equals_pos + 2:]
        temp_c = float(temp_string) / 1000
        return temp_c
    else:
        log.error(f'Erro ao ler temperatura no folder - {folder}')
        return 0


def ler_temperaturas():
    devices = dict()
    for sensor in sensores.keys():
        devices[sensor] = read_temp(sensor)

    devices = converter_codigo_nome(devices)
    # Calibragem aplicada
    devices = calibragem(devices)
    return devices


def calibragem(devices):
    ''' sensor 28-adeb0d1e64ff (tout) = (valor medido -(-1,42759119171347))/1,05231004995341
        sensor 28-16dc0d1e64ff (tfoot) = (valor medido -(-0,99463359768741))/1,04367372803212
        sensor 28-d9a50d1e64ff (tin) = (valor medido -(-1,10163022336359))/1,05032038837543
        sensor 28-37c50d1e64ff (tabd) = (valor medido -(-1,22741034125413))/1,05716280778418
        sensor 28-d9c00d1e64ff (tg) = (valor medido -(-1,21262025963730))/1,05684528754355
    '''

    try:
        devices['tout'] = (devices['tout'] -(-1.42759119171347)) / 1.05231004995341
    except TypeError as te:
        devices['tout'] = None
    try:
        devices['tfoot'] = (devices['tfoot'] - (-0.99463359768741)) / 1.04367372803212
    except TypeError as te:
        devices['tfoot'] = None
    try:
        devices['tin'] = (devices['tin'] - (-1.10163022336359)) / 1.05032038837543
    except TypeError as te:
        devices['tin'] = None
    try:
        devices['tabd'] = (devices['tabd'] - (-1.22741034125413)) / 1.05716280778418
    except TypeError as te:
        devices['tabd'] = None
    try:
        devices['tg'] = (devices['tg'] - (-1.21262025963730)) / 1.05684528754355
    except TypeError as te:
        devices['tg'] = None

    return devices


def converter_codigo_nome(temps):
    novo = {}
    for key, value in sensores.items():
        novo[value] = temps[key]
    return novo


def main():
    temp = ler_temperaturas()
    for s in sensores.values():
        print(f'{s} = {temp[s]}')


if __name__ == '__main__':
    main()
