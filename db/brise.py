from statistics import median
from pony import orm
from datetime import date, time, datetime



# Fabrica de entidades
def define_entidades(**db_params) -> 'Brise':
    db = orm.Database(**db_params)
    class Brise(db.Entity):
        data = orm.Required(date, default=date.today(), index=True)
        hora = orm.Required(time, default=datetime.now().strftime("%H:%M:%S"))
        tin = orm.Optional(float)
        tg = orm.Optional(float)
        tmr = orm.Optional(float)
        tn = orm.Optional(float)
        tn_inf = orm.Optional(float)
        tn_sup = orm.Optional(float)
        tfoot = orm.Optional(float)
        tabd = orm.Optional(float)
        thead = orm.Optional(float)
        tout = orm.Optional(float)
        to = orm.Optional(float)
        e_table_inf = orm.Optional(float)
        e_table_sup = orm.Optional(float)
        e_table = orm.Optional(float, default=0)
        e_eye = orm.Optional(float,  default=0)
        altitude = orm.Optional(float)
        azimute =  orm.Optional(float)
        vsa =  orm.Optional(float)
        teta = orm.Optional(float, default=0)
        teta_fisico = orm.Optional(float, default=0)
        sombreamento = orm.Optional(int, default=0)


        def __str__(self) -> str:
            return str(self.to_dict())

        @orm.db_session
        def ultimo_registro() -> 'Brise':
            return orm.select(s for s in Brise)\
            .order_by(orm.desc(Brise.id))\
            .first()

        @orm.db_session
        def temperatura_neutral() -> float:
            ''' Média das temperaturas dos ultimos 21 dias'''
            N_DIAS = 21
            # return orm.select(orm.avg(medias) for _, medias in 
            #             orm.select(
            #                 (s.data, orm.avg(s.tout)) for s in Brise
            #             ).order_by(lambda: s.data).limit(N_DIAS, 1)
            #         ).get()
            tmp = db.select('''AVG(media) from (
                SELECT AVG("s"."tout") as media
                FROM "Brise" "s"
                GROUP BY "s"."data"
                ORDER BY "s"."data" DESC
                LIMIT $N_DIAS OFFSET 1)'''
            )[0]
            if not tmp:
                tmp = 0
            return 17.8 + 0.31 * tmp

    orm.sql_debug(False)
    db.generate_mapping(create_tables=True)
    return db


if __name__ == '__main__': ## Testes
    db = define_entidades(provider='sqlite', filename='brise.db')
    Brise = db.Brise
    # import timeit
    # print(timeit.timeit(Brise.calcular_tmp, number=100))

    # with orm.db_session:
    b = Brise.ultimo_registro()
    print(b)
