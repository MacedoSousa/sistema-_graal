from servicos.database import conectar_banco_de_dados
from datetime import datetime
from servicos.utils import logar_erro

def obter_vendas_do_mes_atual():
    cnx = conectar_banco_de_dados()
    if cnx is None:
        return 0.0
    try:
        cursor = cnx.cursor()
        hoje = datetime.now()
        primeiro_dia_mes = hoje.replace(day=1).strftime("%Y-%m-%d 00:00:00")
        if hoje.month == 12:
            proximo_mes = hoje.replace(year=hoje.year + 1, month=1, day=1)
        else:
            proximo_mes = hoje.replace(month=hoje.month + 1, day=1)
        ultimo_dia_mes = proximo_mes.strftime("%Y-%m-%d 00:00:00")
        cursor.execute(
            "SELECT SUM(valor_total) FROM venda WHERE data_venda >= ? AND data_venda < ?",
            (primeiro_dia_mes, ultimo_dia_mes)
        )
        total_vendas = cursor.fetchone()[0]
        return total_vendas if total_vendas else 0.0
    except Exception as e:
        logar_erro(e)
        print(f"Erro ao obter vendas do mês atual: {e}")
        return 0.0
    finally:
        if cnx:
            cursor.close()
            cnx.close()

def obter_vendas_mes_atual():
    return obter_vendas_do_mes_atual()

def obter_vendas_do_mes():
    return obter_vendas_do_mes_atual()

def obter_ultimas_vendas(limite=5):
    cnx = conectar_banco_de_dados()
    if cnx is None:
        return []
    try:
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT data_venda, valor_total FROM venda ORDER BY data_venda DESC LIMIT ?", (limite,)
        )
        vendas = [
            {'data': row[0], 'valor': row[1]} for row in cursor.fetchall()
        ]
        return vendas
    except Exception as e:
        logar_erro(e)
        print(f"Erro ao obter últimas vendas: {e}")
        return []
    finally:
        if cnx:
            cursor.close()
            cnx.close()
