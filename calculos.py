import math
from datetime import datetime
from typing import Tuple
from pysolar import solar
import config

from logs.config import *


def calculos_coordenadas():
    agora = datetime.now()
    agora = agora.replace(tzinfo=config.TIMEZONE)
    altitude = solar.get_altitude(config.LAT, config.LONG, agora)
    azimute = solar.get_azimuth(config.LAT, config.LONG, agora)
    vsa = calculo_vsa({
        'altitude': altitude,
        'azimute': azimute
    })
    coordenadas_solares = {
        'altitude': altitude,
        'azimute': azimute,
        'vsa': vsa
    }

    return coordenadas_solares


def calculo_vsa(coordenadas_solares):
    altitude = coordenadas_solares['altitude']
    azimute = coordenadas_solares['azimute']
    HSA = math.radians(azimute - config.ORI)
    VSA = math.atan(math.tan(math.radians(altitude)) / math.cos(HSA))

    return math.degrees(VSA)


def calcular_sombreamento_teta(e_table, vsa, to, tn, coordenadas_solares, sombreamento) -> int:
    to = to or 0
    tn = tn or 0
    lux = e_table or 0
    agora = datetime.now().time()
    # Horario de funcionamento
    if config.HORA_INICIO <= agora <= config.HORA_FIM:
        if lux > config.MAX_LUX and sombreamento == 100:
            teta = 60
            return (sombreamento, teta)
        if to < tn - 2.5:  # Condicao 1 (sombreamento = 0%)
            log.debug('Condicao 1')
            if lux <= config.MAX_LUX and sombreamento == 0:
                sombreamento = 0
            elif lux > config.MAX_LUX and sombreamento == 0:
                sombreamento = 50
            elif lux < config.MIN_LUX and sombreamento == 50:
                sombreamento = 0
            elif (config.MIN_LUX <= lux <= config.MAX_LUX) and sombreamento == 50:
                sombreamento = 50
            elif lux > config.MAX_LUX and sombreamento == 50:
                sombreamento = 100
            elif (config.MIN_LUX <= lux <= config.MAX_LUX) and sombreamento == 100:
                sombreamento = 100
            elif lux < config.MIN_LUX and sombreamento == 100:
                sombreamento = 50
        elif tn - 2.5 <= to < tn:  # Condicao 2 (sombreamento =  50%)
            log.debug('Condicao 2')
            if sombreamento <= 50 and lux <= config.MAX_LUX:
                sombreamento = 50
            elif sombreamento <= 50 and lux > config.MAX_LUX:
                sombreamento = 100
            elif sombreamento == 100 and config.MIN_LUX <= lux <= config.MAX_LUX:
                sombreamento = 100
            elif sombreamento == 100 and lux < config.MIN_LUX:
                sombreamento = 50
        elif tn <= to < tn + 2.5:  # Condicao 3
            log.debug('Condicao 3')
            sombreamento = 100
        elif to >= tn + 2.5:    # Condicao 4
            log.debug('Condicao 4')
            teta = 60
            sombreamento = 200
            return (sombreamento, teta)

        ######
        # Condicao de radiacao direta e radiacao difusa
        if 0 <= vsa <= 60 and not(config.FORCAR_REGRA_DIFUSA):
            log.debug(f'radiacao direta (vsa={vsa})')
            teta = calcular_teta(coordenadas_solares=coordenadas_solares, lux=e_table, sombreamento=sombreamento)
        else:
            log.debug(f'radiacao difusa (vsa={vsa})FRD={config.FORCAR_REGRA_DIFUSA}')
            teta = calcular_teta_radiacao_difusa(sombreamento=sombreamento)
    else:
        teta = 0
        sombreamento = 0
        log.debug(f'Fora do horario ({agora})')
    return (sombreamento, teta)

def calcular_teta_radiacao_difusa(sombreamento):
    if sombreamento == 0:
        teta = 0
    elif sombreamento == 50:
        teta = 30
    elif sombreamento == 100:
        teta = 60
    log.debug(f'sombreamento={sombreamento}; teta={teta}')
    return teta

def calcular_teta(coordenadas_solares, lux, sombreamento):
    # Fora do horario de funcionamento teta = 0
    agora = datetime.now().time()
    if not(config.HORA_INICIO <= agora <= config.HORA_FIM):
        return 0
    # Calculo vsa
    lux = lux or 0
    vsa = coordenadas_solares['vsa']
    if sombreamento == 0:
        teta = -vsa
        config.espera = True
    elif sombreamento == 50:
        alfa_rad = math.radians(vsa)
        alfa_degree = math.degrees(math.asin(math.cos(alfa_rad) / 2))
        teta = alfa_degree - vsa
        if lux > config.MAX_LUX:
            log.debug(f'S={sombreamento};lux>config.MAX_LUX;teta era={teta})')
            sombreamento = 100
            teta = 90 - 2 * vsa
            if teta < 0:
                log.debug(f'S={sombreamento};lux>config.MAX_LUX;teta<0(teta_era={teta})')
                teta = 0
            config.espera = False
        else:
            config.espera = True
    elif sombreamento == 100:
        teta = 90 - 2 * vsa
        if lux > config.MAX_LUX and not config.espera:
            log.debug(f'S={sombreamento};lux>config.MAX_LUX(teta era={teta})')
            teta = config.MAX_ANGLE
            config.espera = True
        elif teta < 0:
            log.debug(f'S={sombreamento};teta<0(teta era={teta})')
            teta = 0
    # Sempre dentro dos limites
    if (teta < config.MIN_ANGLE):
        log.debug(f'Minimo (era={teta})')
        teta = config.MIN_ANGLE
    elif (teta > config.MAX_ANGLE):
        log.debug(f'Maximo (era={teta})')
        teta = config.MAX_ANGLE

    return teta


def temperatura_operativa_tmr(tin: float, tg: float) -> Tuple[float, float]:
    ''' CÁLCULO DA TEMPERATURA OPERATIVA (To)
    - é medida de 5 em 5 minutos.
    To = (Ta + Tmr) /2.
    Ta = Tin
    Tmr = {[(Tg + 273)^4 + ((1,1*10^8*Va^0,6)/(£*D^0,4))*(Tg-Ta)]^0,25} - 273
    Onde:
    Tg = Temperatura de Globo
    D = diâmetro do globo = 0.07 cm;
    Pound = emissividade do material do globo = 0,92 (chute baseado no google);
    Va - velocidade do ar no interior da câmara = não temos esse valor ainda, considerar um valor qualquer < que 1,0;
    Ta - Temperatura interna na câmara - Sensor 1a2 - Tw7.
    '''
    Ta = tin or 0
    Tg = tg or 0
    Va = 0.03
    emissividade = 0.92
    D = 0.07
    TMR = (((Tg + 273)**4 + ((1.1*(10**8)*(Va**0.6))/(emissividade*(D**0.4)))*(Tg - Ta)) ** 0.25) - 273
    To = (Ta + TMR) / 2
    return (To, TMR)


if __name__ == '__main__':
    print(temperatura_operativa_tmr())
