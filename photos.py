import os
from picamera import PiCamera
from time import sleep
from datetime import datetime
from os.path import exists
from logs.config import *


def save(name):
    date_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    name = f'{date_time}_{name}.jpg'
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (2592, 1944)
    # essa é a resolução máxima. a minima é 64x64
    camera.framerate = 15
    # camera.start_preview(alpha=200)
    sleep(3)
    dir = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(dir, 'camera', 'fotos', name)
    camera.capture(file)
    # camera.stop_preview()
    camera.close()

def condicoes(brise, sombreamento_anterior):
    # Registrar entre 5h e 20h
    HORA_INICIO = datetime.strptime('05:00:00',"%H:%M:%S").time()
    HORA_FIM = datetime.strptime('20:00:00',"%H:%M:%S").time()
    agora = datetime.now().time()
    if not(HORA_INICIO <= agora <= HORA_FIM):
        log.debug(f'Fora do horário de fotos -> {agora}')
        return None
    name = ''
    # print(brise)
    # if brise.to >= (brise.tn + 2.5):
    #     name += 'to-maior-tn-mais2.5;'
    #     # save(name)
    # elif brise.to >= (brise.tn - 2.5):
    #     name += 'to-maior-tn-menos2.5;'
    if abs(brise.tfoot - brise.thead) >= 3:
        name += 'to-maior-tn-menos-2.5;'
    # if brise.e_table < 100:
    #     name += 'e_table-menor-100;'
    if brise.e_table > 2000:
        name += 'e_table-maior-2000;'
    if brise.e_eye > 2000:
        name += 'e_eye-maior-2000;'
    if brise.sombreamento == 0 and sombreamento_anterior == 50:
        name += 'sombreamento-atual-0_anterior-50;'
    elif brise.sombreamento == 50 and sombreamento_anterior == 100:
        name += 'sombreamento-atual-50_anterior-100;'
    elif brise.sombreamento == 50 and sombreamento_anterior == 0:
        name += 'sombreamento-atual-50_anterior-0;'
    elif brise.sombreamento == 100 and sombreamento_anterior == 50:
        name += 'sombreamento-atual-100_anterior-50;'

    if name:
        save(name)


if __name__ == '__main__': ## Testes
    save('teste')


# to      tfoot       e_table     e_eye
# 1       0           0           0
# 1       0           1           0
# 1       0           0           1
# 1       0           1           1
# 1       1           0           0
# 1       1           0           1
# 1       1           1           0
# 1       1           1           1
# 0       0           1           0
# 0       0           0           1
# 0       0           1           1
# 0       1           0           0
# 0       1           0           1
# 0       1           1           0
# 0       1           1           1
