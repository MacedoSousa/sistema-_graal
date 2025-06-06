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
        cursor.execute("SELECT cpf_cliente, valor_total, forma_pagamento, data_venda FROM venda WHERE id_pedido = ? ORDER BY data_venda DESC LIMIT 1", (id_pedido,))
        venda = cursor.fetchone()
        if not venda:
            cursor.close()
            return None
        cpf_cliente, valor_total, forma_pagamento, data_venda = venda
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
            'forma_pagamento': forma_pagamento,
            'data_venda': data_venda
        }
    finally:
        conn.close()

def listar_recibos():
    recibos = []
    for r in listar_comandas_fechadas():
        conn = conectar_banco_de_dados()
        funcionario_nome = ''
        data_venda = r.get('data_venda', '')
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.nome FROM pedido p
                JOIN funcionario f ON p.id_funcionario = f.id_funcionario
                WHERE p.id_pedido = ?
            """, (r['id_pedido'],))
            row = cursor.fetchone()
            if row:
                funcionario_nome = row[0]
        except Exception:
            funcionario_nome = ''
        finally:
            conn.close()
        recibos.append({
            'id_pedido': r['id_pedido'],
            'valor_total': r['valor_total'],
            'data_venda': data_venda,
            'cpf_cliente': r['cpf_cliente'],
            'forma_pagamento': r['forma_pagamento'],
            'funcionario': funcionario_nome
        })
    return recibos

def gerar_recibo_detalhado(recibo):
    funcionario = recibo.get('funcionario', '-')
    valor_total = recibo.get('valor_total', 0)
    forma_pagamento = recibo.get('forma_pagamento', '-')
    data_venda = recibo.get('data_venda', '-')
    cpf_cliente = recibo.get('cpf_cliente', '-')
    detalhes = f"""
Recibo de Compra
--------------------------
Funcionário: {funcionario}
CPF Cliente: {cpf_cliente}
Data da Venda: {data_venda}
Forma de Pagamento: {forma_pagamento}
Valor Total: R$ {valor_total:.2f}
--------------------------"""
    return detalhes

def gerar_recibo_detalhado(id_pedido):
    conn = conectar_banco_de_dados()
    if conn is None:
        return "Recibo não disponível."
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.cpf_cliente, v.valor_total, v.forma_pagamento, v.data_venda, f.nome
            FROM venda v
            JOIN pedido p ON v.id_pedido = p.id_pedido
            JOIN funcionario f ON p.id_funcionario = f.id_funcionario
            WHERE v.id_pedido = ?
            ORDER BY v.data_venda DESC LIMIT 1
        """, (id_pedido,))
        venda = cursor.fetchone()
        if not venda:
            cursor.close()
            return "Recibo não encontrado."
        cpf_cliente, valor_total, forma_pagamento, data_venda, funcionario_nome = venda
        cursor.execute("""
            SELECT pr.nome, ip.quantidade, ip.preco_unitario
            FROM item_pedido ip
            JOIN produto pr ON ip.id_produto = pr.id_produto
            WHERE ip.id_pedido = ?
        """, (id_pedido,))
        produtos = cursor.fetchall()
        cursor.close()
        produtos_texto = "\n".join(f"{nome} x {quantidade} - R$ {preco:.2f}" for nome, quantidade, preco in produtos)
        recibo = f"""
        GRAAL BAR
        -----------------------------
        Funcionário: {funcionario_nome}
        Data: {data_venda}
        CPF Cliente: {cpf_cliente}
        Forma de Pagamento: {forma_pagamento}
        -----------------------------
        Produtos:
        {produtos_texto}
        -----------------------------
        TOTAL: R$ {valor_total:.2f}
        """
        return recibo.strip()
    finally:
        conn.close()