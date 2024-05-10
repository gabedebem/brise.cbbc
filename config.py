from datetime import datetime, timezone, timedelta
from local_config import *

# Funcionar brise (True) apenas coletar dados (False)
FUNCIONAR_BRISE = True

## Constantes
FORCAR_REGRA_DIFUSA = False
# Aprox 6s de delay
TEMPO_ESPERA = 595
MIN_LUX = 100
MAX_LUX = 2000
MIN_ANGLE = -70
MAX_ANGLE = 70
# limites fisicos do BRISEgit
MIN_TETA_FISICO = -60
MAX_TETA_FISICO = 60
# Localizacao, TimeZone de Curitiba e orientacao da camara
LAT = -25.4429402
LONG = -49.3539662
TIMEZONE = timezone(timedelta(hours=-3))
ORI = 0
HORA_INICIO = datetime.strptime('07:00:00', "%H:%M:%S").time()
HORA_FIM = datetime.strptime('18:00:00', "%H:%M:%S").time()
# Se precisa calibrar o brise
CALIBRAR = False
# TODO: revisar constantes
espera = True

#pwm_servo = 3
# TMR = 0
# sombreamento = 0
# # Brise
# Teta = 0
