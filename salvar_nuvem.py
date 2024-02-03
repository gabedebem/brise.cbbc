import gspread
from logs.config import *
from pony import orm

def conectar():
    # # gambiarra para o requests do google funcionar
    # import requests
    # requests.utils.NETRC_FILES=[]
    # Conectar
    gc = gspread.service_account()
    # Encontrar planilha
    sh = gc.open("CBBC")
    # Encontrar primeira aba
    ws = sh.worksheet('brise')
    return ws

@orm.db_session
def salvar_dados_nuvem(dados):
    try:
        ws = conectar()
    except Exception as e:
        log.error('Erro ao conectar na API do Google')
        log.exception(e)
    else:
        try:
            ws.append_row(dados)
        except Exception as e:
            log.error('Erro ao salvar dados na nuvem')
            log.exception(e)


        ## Salvar dados na planilha em nuvem
        # data_hora = f"{brise.data} {brise.hora}"
        # debug = None
        # salvar_dados_nuvem([
        #         data_hora, brise.tin, brise.tg, brise.tout, brise.tfoot, brise.tabd, brise.tmr, brise.to, brise.tn, brise.e_table, brise.e_eye, brise.altitude,
        #         brise.azimute, brise.sombreamento, brise.teta, debug
        # ])
        # log.debug(f'Dados inseridos na planilha')