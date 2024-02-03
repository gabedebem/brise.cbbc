#!/usr/bin/python3
from pony import orm
from pysolar import solar
from datetime import datetime, timezone, timedelta

from db.brise import define_entidades
import calculos
import config
# import lux
# import salvar_nuvem

#
### DEPRECIADO  !! ###
#

db = define_entidades(provider='sqlite', filename='test_mock_leitura.db')
Brise = db.Brise
brise = Brise.ultimo_registro()
agora = datetime.now()
agora = agora.replace(config.TIMEZONE)
altitude = solar.get_altitude(config.LAT, config.LONG, agora)
azimute = solar.get_azimuth(config.LAT, config.LONG, agora)
to = calculos.temperatura_operativa_tmr(tin=brise.tin, tg=brise.tg)
tn = db.Brise.temperatura_neutral()

## TODO: ler temp. ler lux, ler co2, calculos de sombreamento, teta, alfa, etc
## Testes
temps = {'tg': 321.321, 'tin': 643.3, 'tout': 798.3}
lux = {'in': 123, 'out': 2}
pwm_servo = sombreamento = co2 = alfa = teta = 0

# Salvar no BD
with orm.db_session:
    b = Brise(
        tg=temps['tg'],
        tin=temps['tin'],
        tout=temps['tout'],
        lux_in=lux['in'],
        lux_out=lux['out'],
        co2=co2,
        to=to,
        tn=tn,
        alfa=alfa,
        teta=teta,
        altitude=altitude,
        azimute=azimute,
        pwm_servo=pwm_servo,
        sombreamento=sombreamento,
    )
    print(f'Leitura dos dados realizada com sucesso - {b.data}{b.hora}')

# Salvar Nuvem
# salvar_nuvem.salvar_temps_nuvem()

