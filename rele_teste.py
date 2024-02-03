#!/usr/bin/python3
import rele
import RPi.GPIO as GPIO
import time
from logs.config import *
import sys


GPIO.setmode(GPIO.BCM)
# init list with pin numbers
pins = [5, 6]
# loop through pins and set mode and state to 'low'
for i in pins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)


def girar(tempo_acionamento) -> None:
    GPIO.setmode(GPIO.BCM)
    if tempo_acionamento < 0: # aciona GPIO 6 - SOBE
        try:
            GPIO.setup(6, GPIO.OUT)
            GPIO.output(6, GPIO.LOW)
            log.debug(f'Girando rele PIN 6 por {tempo_acionamento}s')
            tempo_acionamento *= -1 # troca sinal
            time.sleep(tempo_acionamento)
            log.debug("Girou")
        finally:
            GPIO.setup(6, GPIO.OUT)
            GPIO.output(6, GPIO.HIGH)

    elif tempo_acionamento > 0: # aciona GPIO 5 - DESCE
        try:
            GPIO.setup(5, GPIO.OUT)
            GPIO.output(5, GPIO.LOW)
            log.debug(f'Girando rele PIN 5 por {tempo_acionamento}s')
            time.sleep(tempo_acionamento)
            log.debug("Girou")
        finally:
            GPIO.setup(5, GPIO.OUT)
            GPIO.output(5, GPIO.HIGH)
    GPIO.cleanup()



if __name__ == '__main__':
    tempo_acionamento = float(sys.argv[1])
    if tempo_acionamento == 0:
        print('Calibrando')
        rele.calibrar()
    else:
        print(f'tempo = {tempo_acionamento}')
        girar(tempo_acionamento)