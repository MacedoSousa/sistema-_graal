from servicos.database import conectar_banco_de_dados
from servicos.utils import logar_erro
import sqlite3

def obter_total_de_produtos():
    conexao = conectar_banco_de_dados()
    if conexao is None:
        return 0
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM produto")
        return cursor.fetchone()[0]
    except Exception as e:
        logar_erro(e)
        print(f"Erro ao obter total de produtos: {e}")
        return 0
    finally:
        conexao.close()

def obter_produtos_em_baixo_estoque():
    conexao = conectar_banco_de_dados()
    if conexao is None:
        return []
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, estoque FROM produto WHERE estoque < 5")
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logar_erro(e)
        print(f"Erro ao obter produtos em baixo estoque: {e}")
        return []
    finally:
        conexao.close()

def salvar_novo_produto(produto):
    conexao = conectar_banco_de_dados()
    if conexao is None:
        return
    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT INTO produto 
            (nome, codigo_de_barras, preco, data_validade, peso_kg, fornecedor, estoque) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                produto["nome"],
                produto["codigo_de_barras"],
                produto["preco"],
                produto["data_validade"],
                produto["peso_kg"],
                produto["fornecedor"],
                produto["estoque"]
            )
        )
        conexao.commit()
    except Exception as e:
        print(f"Erro ao salvar produto: {e}")
    finally:
        conexao.close()

def atualizar_produto(conn, produto):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produto
        SET nome = ?, fornecedor = ?, peso_kg = ?, preco = ?, data_validade = ?, estoque = ?, codigo_de_barras = ?
        WHERE id_produto = ?
    """, (produto["nome"], produto["fornecedor"], produto["peso_kg"], produto["preco"],
          produto["data_validade"], produto["estoque"], produto['codigo_de_barras'], produto["id_produto"]))


def excluir_produto(produto_id):
    conexao = conectar_banco_de_dados()
    if conexao is None:
        return False
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produto WHERE id_produto = ?", (produto_id,))
        conexao.commit()
        return True
    except Exception as e:
        print(f"Erro ao excluir produto: {e}")
        return False
    finally:
        conexao.close()

def obter_todos_os_produtos(conexao):
    if conexao is None:
        return []
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produto")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter todos os produtos: {e}")
        return []

def obter_proximo_codigo(conexao):
    if conexao is None:
        return 1
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id_produto FROM produto ORDER BY id_produto DESC LIMIT 1")
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0] + 1
        else:
            return 1 
    except Exception as e:
        print(f"Erro ao obter próximo código: {e}")
        return 1


def obter_todos_os_produtos_dict():
    conexao = conectar_banco_de_dados()
    if conexao is None:
        return []
    try:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT id_produto, codigo_de_barras, nome, fornecedor, peso_kg, preco, data_validade, estoque 
            FROM produto
        """)
        produtos = []
        for row in cursor.fetchall():
            produtos.append({
                'id': row['id_produto'],
                'codigo_barras': row['codigo_de_barras'],
                'nome': row['nome'],
                'empresa': row['fornecedor'],
                'peso': row['peso_kg'],
                'unidade': '',  # Preencher se houver campo na tabela
                'preco': row['preco'],
                'validade': row['data_validade'],
                'quantidade': row['estoque']
            })
        return produtos
    except Exception as e:
        print(f"Erro ao obter produtos como dicionário: {e}")
        return []
    finally:
        conexao.close()

def obter_produto_por_codigo(codigo_produto):
    conexao = conectar_banco_de_dados()
    if conexao is None:
        return None
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produto WHERE id_produto = ?", (codigo_produto,))
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"Erro ao obter produto por código: {e}")
        return None
    finally:
        conexao.close()

def checar_estoque(id_produto, quantidade):
    conexao = conectar_banco_de_dados()
    if conexao is None:
        return False
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT estoque FROM produto WHERE id_produto = ?", (id_produto,))
        resultado = cursor.fetchone()
        if resultado and resultado[0] >= quantidade:
            return True
        return False
    except Exception as e:
        print(f"Erro ao checar estoque: {e}")
        return False
    finally:
        conexao.close()

def atualizar_estoque(id_produto, quantidade_vendida):
    conexao = conectar_banco_de_dados()
    if conexao is None:
        return False
    try:
        cursor = conexao.cursor()
        cursor.execute("UPDATE produto SET estoque = estoque - ? WHERE id_produto = ? AND estoque >= ?", (quantidade_vendida, id_produto, quantidade_vendida))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar estoque: {e}")
        return False
    finally:
        conexao.close()

def listar_produtos():
    """Compatibilidade: retorna todos os produtos como lista de dicionários."""
    return obter_todos_os_produtos_dict()

def salvar_produto(produto):
    """Compatibilidade: salva um novo produto."""
    return salvar_novo_produto(produto)
