#!/usr/bin/python3
import time
from datetime import datetime
from pony import orm

from db.brise import define_entidades
from logs.config import *
from sensores_temperatura import ler_temperaturas
from lux import ler_lux
import photos
import config
import calculos
import rele

def main():
    # db = define_entidades(provider='sqlite', filename='test_mock_leitura.db', create_db=True)
    db = define_entidades(provider='sqlite', filename='brise.db', create_db=True)
    Brise = db.Brise
    with orm.db_session:
        brise = Brise.ultimo_registro()
    log.debug(f'Leitura do brise -> {brise}')
    coordenadas_solares = calculos.calculos_coordenadas()
    altitude = coordenadas_solares['altitude']
    azimute = coordenadas_solares['azimute']
    vsa = calculos.calculo_vsa(coordenadas_solares)
    coordenadas_solares['vsa'] = vsa
    temps = ler_temperaturas()
    try:
        to, tmr = calculos.temperatura_operativa_tmr(tin=temps.get('tin'), tg=temps.get('tg'))
    except AttributeError as e:
        log.error(f'Erro ao fazer leitura do ultimo registro (BD vazio?) -> Erro: {e}')
        to, tmr = calculos.temperatura_operativa_tmr(tin=0, tg=0)
    tn = Brise.temperatura_neutral()
    log.debug(f'Calculos -> alt={altitude}; az={azimute}; vsa={vsa}; to={to}; tn={tn}')

    lux = ler_lux()
    teta_inicial = brise.teta_fisico
    sombreamento_anterior = brise.sombreamento
    sombreamento, teta = calculos.calcular_sombreamento_teta(
        e_table=lux.get('e_table'),
        vsa=vsa,
        to=to,
        tn=tn, 
        coordenadas_solares=coordenadas_solares,
        sombreamento=sombreamento_anterior
    )

    teta_fisico = teta
    if teta > config.MAX_TETA_FISICO:
        teta_fisico = config.MAX_TETA_FISICO
    elif teta < config.MIN_TETA_FISICO:
        teta_fisico = config.MIN_TETA_FISICO

    # Salvar no BD
    with orm.db_session:
        brise = Brise(
            tg=temps.get('tg'),
            tin=temps.get('tin'),
            tout=temps.get('tout'),
            tfoot = temps.get('tfoot'),
            tabd = temps.get('tabd'),
            thead = temps.get('tin'),
            e_table = lux.get('e_table'),
            e_table_sup = 2000,
            e_table_inf = 100,
            e_eye = lux.get('e_eye'),
            to = to,
            tn = tn,
            tn_inf = tn-2.5,
            tn_sup = tn+2.5,
            teta=teta,
            teta_fisico=teta_fisico,
            vsa=vsa,
            altitude=altitude,
            azimute=azimute,
            tmr=tmr,
            sombreamento=sombreamento,
        )
        log.debug(f'Dados inseridos no BD')
        ## Condicoes das fotos
        photos.condicoes(brise, sombreamento_anterior)

    ## Girar brise
    agora = datetime.now().time()
    if config.HORA_INICIO <= agora <= config.HORA_FIM:
        rele.girar(teta_inicial, teta_fisico)
        config.CALIBRAR = True
    else:
        log.debug('Fora do horário de funcionamento.')
        if config.CALIBRAR:
            rele.calibrar()
            log.debug('Calibrando...')
            config.CALIBRAR = False

if __name__ == '__main__':
    # Insere brise na posicao anterior
    rele.calibrar()
    db = define_entidades(provider='sqlite', filename='brise.db')
    Brise = db.Brise
    with orm.db_session:
        brise = Brise.ultimo_registro()

    if brise.teta_fisico:
        log.debug(f'Insere na posicao anterior ({brise.teta_fisico})')
        rele.girar(0, brise.teta_fisico)

    # Loop principal
    try:
        while True:
            log.info('Executando main...')
            main()
            time.sleep(config.TEMPO_ESPERA)
    except Exception as e:
            log.error('Global try catch handler')
            log.exception(e)
    finally:
        if not config.DEBUG:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.cleanup()
