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
