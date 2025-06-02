from servicos.database import conectar_banco_de_dados
from datetime import datetime
import sqlite3

def obter_comandas_abertas():
    conn = conectar_banco_de_dados()
    if conn is None:
        return {}

    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = """
            SELECT
                p.id_pedido AS comanda_id,
                pr.nome AS produto_nome,
                ip.quantidade,
                ip.preco_unitario
            FROM pedido p
            LEFT JOIN item_pedido ip ON p.id_pedido = ip.id_pedido
            LEFT JOIN produto pr ON ip.id_produto = pr.id_produto
            WHERE p.status = 'aberta'
            ORDER BY p.id_pedido
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        comandas = {}
        for row in resultados:
            comanda_id = row["comanda_id"]
            if comanda_id not in comandas:
                comandas[comanda_id] = []
            if row["produto_nome"] is not None:
                comandas[comanda_id].append({
                    "produto_nome": row["produto_nome"],
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"]
                })

        cursor.execute("SELECT id_pedido FROM pedido WHERE status = 'aberta'")
        todas_abertas = [row[0] for row in cursor.fetchall()]
        for comanda_id in todas_abertas:
            if comanda_id not in comandas:
                comandas[comanda_id] = []
        return comandas
    except Exception as e:
        print(f"Erro ao obter comandas abertas: {e}")
        return {}
    finally:
        if conn:
            cursor.close()
            conn.close()

def abrir_nova_comanda():
    conn = conectar_banco_de_dados()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        data_pedido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO pedido (data_pedido, status) VALUES (?, ?)"
        cursor.execute(query, (data_pedido, 'aberta'))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        print(f"Erro ao abrir nova comanda: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def adicionar_item_a_comanda(numero_comanda, produto, quantidade):
    conn = conectar_banco_de_dados()
    if conn is None:
        raise Exception("Não foi possível conectar ao banco de dados.")

    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query_produto = "SELECT preco, nome FROM produto WHERE id_produto = ?"
        cursor.execute(query_produto, (produto['id_produto'],))
        produto_db = cursor.fetchone()

        if not produto_db:
            raise Exception(f"Produto com ID {produto['id_produto']} não encontrado.")

        preco_unitario = produto_db["preco"]

        query_item = """
            INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(query_item, (numero_comanda, produto['id_produto'], quantidade, preco_unitario))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Erro ao adicionar item à comanda: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def obter_comanda(numero_comanda):
    conn = conectar_banco_de_dados()
    if conn is None:
        return None

    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = """
            SELECT
                p.id_pedido AS comanda_id,
                p.status,
                pr.nome AS produto_nome,
                ip.quantidade,
                ip.preco_unitario
            FROM pedido p
            JOIN item_pedido ip ON p.id_pedido = ip.id_pedido
            JOIN produto pr ON ip.id_produto = pr.id_produto
            WHERE p.id_pedido = ?
            and p.status != 'fechada'
            ORDER BY pr.nome
        """
        cursor.execute(query, (numero_comanda,))
        resultados = cursor.fetchall()

        if not resultados:
            return None

        comanda = {
            "numero_comanda": numero_comanda,
            "status": resultados[0]["status"],
            "itens": []
        }

        for row in resultados:
            comanda["itens"].append({
                "produto_nome": row["produto_nome"],
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"]
            })

        return comanda
    except Exception as e:
        print(f"Erro ao obter comanda: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def excluir_comanda(numero_comanda):
    conn = conectar_banco_de_dados()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedido WHERE id_pedido = ?", (numero_comanda,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir comanda: {e}")
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

def fechar_comanda(numero_comanda):
    conn = conectar_banco_de_dados()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE pedido SET status = 'fechada' WHERE id_pedido = ?", (numero_comanda,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao fechar comanda: {e}")
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()
