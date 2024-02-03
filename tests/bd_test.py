import pytest
from datetime import date
from pony import orm

from db import brise


@pytest.fixture
def sensores():
    return [
        {'tmr': 96,'tg': 1.1, 'tin': 2.1, 'tout': 3.1, 'e_table': 4.1, 'e_eye': 5.1, 'co2': 6.1, 'to': 8.1, 'tn': 9.1, 'alfa': 10.1, 'teta': 11.1, 'altitude': 12.1, 'azimute': 13.1, 'sombreamento': 15, 'data': date(2022,8,16), 'hora': '16:26:00'},
        {'tmr': 96,'tg': 21.1, 'tin': 22.1, 'tout': 23.1, 'e_table': 24.1, 'e_eye': 25.1, 'co2': 26.1, 'to': 28.1, 'tn': 29.1, 'alfa': 210.1, 'teta': 211.1, 'altitude': 212.1, 'azimute': 213.1, 'sombreamento': 215, 'data': date(2022,8,17), 'hora': '15:26:00'},
        {'tmr': 96,'tg': 2.1, 'tin': 33.1, 'tout': 4.1, 'e_table': 55.1, 'e_eye': 66.1, 'co2': 226.1, 'to': 238.1, 'tn': 239.1, 'alfa': 230.1, 'teta': 31.1, 'altitude': 232.1, 'azimute': 233.1, 'sombreamento': 235, 'data': date(2022,8,21), 'hora': '11:15:20'}
    ]

def test_inserir_temps(sensores):
    db = brise.define_entidades(provider='sqlite', filename=':memory:')
    Brise = db.Brise
    # Inserir fixtures
    with orm.db_session:
        for s in sensores:
            Brise(**s)
        # Numero de rows
        assert Brise.select().count() == len(sensores)
    # Verifica as insercoes
    with orm.db_session:
        # Retorna uma LISTA ([:]) dos objetos
        brises = orm.select(b for b in Brise).order_by(Brise.id)
        # print(brises.get_sql())
        i = 0
        for s in brises:
            assert s.to_dict(exclude='id') == sensores[i]
            i += 1
    with orm.db_session:
        # verifica o primeiro
        first = Brise.select().first()
        assert first.to_dict(exclude='id') == sensores[0]
        # verifica o ultimo
        last = Brise.ultimo_registro()
        assert last.to_dict(exclude='id') == sensores[-1]



# def test_useless(sensores):
#     db = brise.define_entidades(provider='sqlite', filename=':memory:', create_db=True)
#     Brise = db.Brise
#     with orm.db_session:
#         for _ in range(9999):
#             for s in sensores:
#                 Brise(**s)
