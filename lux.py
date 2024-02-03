#!/usr/bin/python3
import time
import board
import adafruit_bh1750
from bh1750 import read_light

from logs.config import *

def ler_lux():
    try:
        i2c = board.I2C()
        # time.sleep(1)
        e_table = adafruit_bh1750.BH1750(i2c, address=0x23)
        e_eye = adafruit_bh1750.BH1750(i2c, address=0x5C)

        return {
            'e_table': e_table.lux,
            'e_eye': e_eye.lux
        }
    except Exception as e:
        log.error('Erro no sensor de Lux')
        log.exception(e)
        return {
            'e_table': 0,
            'e_eye': 0
        }


def main():
    while True:
        print(ler_lux())
        # print(read_light(0x23))
        # print(read_light(0x5C))
        time.sleep(30)


if __name__ == "__main__":
    main()