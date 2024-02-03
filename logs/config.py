import logging
import os
import zlib
from logging.handlers import RotatingFileHandler


# Descompactar com o comando
# zlib-flate -uncompress < logs_sistema.log.3.gz > log3.log 
# Instalar zlib-flate
# sudo apt-get install qpdf


def namer(name):
    return name + ".gz"


def rotator(source, dest):
    print(f'compressing {source} -> {dest}')
    with open(source, "rb") as sf:
        data = sf.read()
        compressed = zlib.compress(data, 9)
        with open(dest, "wb") as df:
            df.write(compressed)
    os.remove(source)


dir = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(dir, 'logs_sistema.log')

logging.basicConfig(
    filename=file,
    level=logging.DEBUG,
    # level=logging.INFO,
    format='%(asctime)s %(levelname)s %(module)s(%(funcName)s): %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
# Handlers configs
handler = RotatingFileHandler(file, maxBytes=20485760, backupCount=3)
handler.rotator = rotator
handler.namer = namer
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s(%(funcName)s): %(message)s')
handler.setFormatter(formatter)
logging.getLogger(__name__).addHandler(handler)
log = logging.getLogger()
log.propagate = False


if __name__ == "__main__":
    for _ in range(1):
        log.debug('Erro de teste')