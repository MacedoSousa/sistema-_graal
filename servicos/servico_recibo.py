from datetime import datetime
from servicos.database import conectar_banco_de_dados

def gerar_recibo_dados(id_pedido, cpf_cliente, produtos, valor_total, forma_pagamento):
    now = datetime.now()
    data_formatada = now.strftime("%d/%m/%Y %H:%M:%S")
    produtos_texto = "\n".join(f"{p['nome']} x {p['quantidade']} - R$ {p['preco']:.2f}" for p in produtos)

    return {
        "data": data_formatada,
        "pedido": id_pedido,
        "cpf_cliente": cpf_cliente,
        "produtos_texto": produtos_texto,
        "total": f"R$ {valor_total:.2f}",
        "pagamento": forma_pagamento,
    }

def listar_comandas_fechadas():
    conn = conectar_banco_de_dados()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id_pedido, v.data_venda, v.valor_total, v.cpf_cliente, v.forma_pagamento
            FROM venda v
            JOIN pedido p ON v.id_pedido = p.id_pedido
            WHERE p.status = 'fechada'
            ORDER BY v.data_venda DESC
        """)
        comandas = [
            {
                'id_pedido': row[0],
                'data_venda': row[1],
                'valor_total': row[2],
                'cpf_cliente': row[3],
                'forma_pagamento': row[4]
            }
            for row in cursor.fetchall()
        ]
        cursor.close()
        return comandas
    finally:
        conn.close()

def obter_dados_recibo(id_pedido):
    conn = conectar_banco_de_dados()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT cpf_cliente, valor_total, forma_pagamento FROM venda WHERE id_pedido = ? ORDER BY data_venda DESC LIMIT 1", (id_pedido,))
        venda = cursor.fetchone()
        if not venda:
            cursor.close()
            return None
        cpf_cliente, valor_total, forma_pagamento = venda
        cursor.execute("""
            SELECT pr.nome, ip.quantidade, ip.preco_unitario
            FROM item_pedido ip
            JOIN produto pr ON ip.id_produto = pr.id_produto
            WHERE ip.id_pedido = ?
        """, (id_pedido,))
        produtos = [
            {'nome': row[0], 'quantidade': row[1], 'preco': row[2]}
            for row in cursor.fetchall()
        ]
        cursor.close()
        return {
            'id_pedido': id_pedido,
            'cpf_cliente': cpf_cliente,
            'produtos': produtos,
            'valor_total': valor_total,
            'forma_pagamento': forma_pagamento
        }
    finally:
        conn.close()

def listar_recibos():
    """Retorna lista de recibos para uso no front unificado."""
    return [
        {'id': r['id_pedido'], 'valor': r['valor_total']} for r in listar_comandas_fechadas()
    ]