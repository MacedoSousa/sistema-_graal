import sqlite3
from datetime import datetime
from servicos.database import conectar_banco_de_dados
from servicos.utils import logar_erro

def registrar_pagamento(numero_comanda, cpf_cliente, valor_total, forma_pagamento):
    cnx = conectar_banco_de_dados()
    if cnx is None:
        raise Exception("Não foi possível conectar ao banco de dados.")

    try:
        cursor = cnx.cursor()

        cursor.execute("SELECT status FROM pedido WHERE id_pedido = ?", (numero_comanda,))
        status = cursor.fetchone()
        if not status:
            raise Exception(f"Comanda {numero_comanda} não encontrada.")
        if status[0] != "aberta":
            raise Exception(f"Comanda {numero_comanda} já está fechada.")

        query_venda = """
            INSERT INTO venda (id_pedido, data_venda, cpf_cliente, valor_total, forma_pagamento)
            VALUES (?, ?, ?, ?, ?)
        """
        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = cursor.execute(query_venda, (numero_comanda, data_venda, cpf_cliente, valor_total, forma_pagamento))

        if result.rowcount == 0:
            raise Exception("Erro ao registrar venda. Nenhuma linha afetada.")
        
        query_status = "UPDATE pedido SET status = 'fechada' WHERE id_pedido = ?"
        cursor.execute(query_status, (numero_comanda,))

        cnx.commit()
        return True
    except Exception as e:
        cnx.rollback()
        logar_erro(e)
        print(f"Erro ao registrar pagamento: {e}")
        return False
    finally:
        if cnx:
            cursor.close()
            cnx.close()
