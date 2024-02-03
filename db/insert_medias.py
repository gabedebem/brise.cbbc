from pony import orm
from brise import define_entidades


db = define_entidades(provider='sqlite', filename='brise.db', create_db=True)
Brise = db.Brise

medias = {
    '2023-07-21': 15.63636081
}

with orm.db_session:
    for data, tout in medias.items():
        # print(f'{data=}; {tout=}')
        b = Brise(
            tout=tout,
            data=data,
            hora='00:00:00',
            e_table=0,
            e_eye=0,
        )



# INSERT INTO 
#     Brise(tout, data, hora)
# VALUES
#     (, '', '00:00:00'),