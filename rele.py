#!/usr/bin/python3
from datetime import datetime
import RPi.GPIO as GPIO
import time
from logs.config import *
import config


GPIO.setmode(GPIO.BCM)
# init list with pin numbers
pins = [5, 6]
# loop through pins and set mode and state to 'low'
for i in pins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)


def girar(teta_inicial, teta_final) -> None:
    GPIO.setmode(GPIO.BCM)
    if teta_inicial > config.MAX_TETA_FISICO:
        teta_inicial = config.MAX_TETA_FISICO
    elif teta_inicial < config.MIN_TETA_FISICO:
        teta_inicial = config.MIN_TETA_FISICO
    if teta_final > config.MAX_TETA_FISICO:
        teta_final = config.MAX_TETA_FISICO
    elif teta_final < config.MIN_TETA_FISICO:
        teta_final = config.MIN_TETA_FISICO    
    tempo_acionamento = 4.2 * (teta_final - teta_inicial) / 201.6
    if tempo_acionamento < 0: # aciona GPIO 6 - SOBE
        try:
            GPIO.setup(6, GPIO.OUT)
            GPIO.output(6, GPIO.LOW)
            log.debug(f'Girando rele PIN 6 por {tempo_acionamento}s ({teta_inicial} -> {teta_final})')
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
            log.debug(f'Girando rele PIN 5 por {tempo_acionamento}s ({teta_inicial} -> {teta_final})')
            time.sleep(tempo_acionamento)
            log.debug("Girou")
        finally:
            GPIO.setup(5, GPIO.OUT)
            GPIO.output(5, GPIO.HIGH)
    GPIO.cleanup()


# Calibracao inicial do Brise
def calibrar():
    GPIO.setmode(GPIO.BCM)
    try:
        GPIO.setup(5, GPIO.OUT)
        GPIO.output(5, GPIO.LOW)
        log.debug(f'Calibrando rele PIN 5 por 4s')
        time.sleep(4)
        log.debug("Girou")
    finally:
        GPIO.setup(5, GPIO.OUT)
        GPIO.output(5, GPIO.HIGH)
        GPIO.cleanup()
    time.sleep(1)
    girar(config.MAX_TETA_FISICO, 0)


if __name__ == '__main__':
    calibrar()

    from pony import orm
    from db.brise import define_entidades
    db = define_entidades(provider='sqlite', filename='brise.db')
    Brise = db.Brise
    with orm.db_session:
        brise = Brise.ultimo_registro()

    log.debug(f'Insere na posicao anterior ({brise.teta_fisico})')
    girar(0, brise.teta_fisico)