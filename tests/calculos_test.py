# import pytest
# from datetime import date
from pony import orm

from db import brise
import calculos

def test_calculos():
    db = brise.define_entidades(provider='sqlite', filename='test.db')
    Brise = db.Brise
    b = Brise.ultimo_registro()

    # tmp = Brise.calcular_tmp()
    # assert tmp == 2
    neutral = Brise.temperatura_neutral()
    assert neutral == 18.42
    to, tmr = calculos.temperatura_operativa_tmr(tin=b.tin, tg=b.tg)
    assert to == 6
    assert tmr == 6

    # assert duck_temps == dict(temps)
    # TO, tmr = temperatura_operativa_tmr(temps)
    # assert TO == 22.0393040570829
    # assert tmr == 21.968119780208724
    # TN = temperatura_neutral()
    # assert TN == 23.266858624004136
    # trm = calcular_trm()
    # assert trm == 17.63502781936818
    # con.close()

