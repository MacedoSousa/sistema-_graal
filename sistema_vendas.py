import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from telas.tela_inicial import TelaInicial
from telas.tela_produtos import TelaProdutos
from telas.tela_comandas import TelaComandas
from telas.tela_pagamento import TelaPagamento
from telas.tela_recibo import TelaRecibo
from telas.tela_login import iniciar_tela_login
from servicos.database import conectar_banco_de_dados, inicializar_banco
from servicos.servico_funcionarios import inicializar_cargos
import platform
import os
import sys

def validar_arquivo_sql(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        print(f"Erro: O arquivo de banco '{nome_arquivo}' não existe.")
        return False
    if not nome_arquivo.lower().endswith(".db"):
        print(f"Erro: O arquivo '{nome_arquivo}' não é um banco SQLite válido.")
        return False
    return True

class SistemaVendas(ttk.Window):
    def __init__(self, usuario_logado):
        super().__init__(themename="flatly")
        self.title("Graal")
        self.geometry("1320x720")
        self.resizable(True, True)
        self.usuario_logado = usuario_logado
        self.configure(bg="#fffbe6")

        self.conn = conectar_banco_de_dados()
        if self.conn is None:
            print("Não foi possível conectar ao banco de dados. O sistema será encerrado.")
            self.destroy()
            return

        # Sidebar
        self.sidebar = ttk.Frame(self, width=220, bootstyle="dark")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Cabeçalho no topo
        self.header = ttk.Frame(self, height=56, bootstyle="light")
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        usuario = self.usuario_logado.get('nome', 'Usuário')
        cargo = self.usuario_logado.get('cargo', 'Cargo')
        self.label_usuario = ttk.Label(self.header, text=f"Usuário: {usuario}  |  Cargo: {cargo}", font=("Arial", 13, "bold"), bootstyle="primary")
        self.label_usuario.pack(side="left", padx=24)
        self.btn_logout = ttk.Button(self.header, text="Logout", bootstyle="danger", width=10, command=self.logout)
        self.btn_logout.pack(side="right", padx=24)

        self.main_frame = ttk.Frame(self, bootstyle="light")
        self.main_frame.pack(side="right", fill="both", expand=True)

        icones = {
            'inicial': '\u2302',
            'produtos': '\u25A3',
            'comandas': '\u270D',
            'pagamento': '\u2708',
            'recibo': '\u270D',
        }

        self.botoes_menu = {}
        self.telas = {}
        self.tela_atual = None

        self.telas['inicial'] = TelaInicial(self.main_frame)
        self.telas['produtos'] = TelaProdutos(self.main_frame, self.conn)
        self.telas['comandas'] = TelaComandas(self.main_frame, self.conn)
        self.telas['pagamento'] = TelaPagamento(self.main_frame, self.conn)
        self.telas['recibo'] = TelaRecibo(self.main_frame, self.conn)

        cargo = usuario_logado.get("cargo", "")
        menu_itens = [("Inicial", 'inicial')]
        if cargo == "Gerente":
            menu_itens += [("Comandas", 'comandas'), ("Pagamento", 'pagamento'), ("Recibo", 'recibo'), ("Produtos", 'produtos')]
        elif cargo == "Vendedor":
            menu_itens += [("Comandas", 'comandas'), ("Pagamento", 'pagamento'), ("Recibo", 'recibo')]
        elif cargo == "Repositor":
            menu_itens += [("Produtos", 'produtos')]
        else:
            menu_itens = [("Inicial", 'inicial')]

        for idx, (nome, chave) in enumerate(menu_itens):
            texto = f"{icones.get(chave, '')}  {nome}"
            btn = ttk.Button(self.sidebar, text=texto, bootstyle="primary", width=18,
                             command=lambda c=chave: self.mostrar_tela(c))
            btn.pack(pady=(18 if idx == 0 else 8, 0), padx=18, anchor="n")
            self.botoes_menu[chave] = btn

        self.mostrar_tela(menu_itens[0][1])
        self.atualizar_dados_tela_inicial()

    def mostrar_tela(self, chave):
        if self.tela_atual:
            self.telas[self.tela_atual].pack_forget()
        self.telas[chave].pack(fill="both", expand=True)
        self.tela_atual = chave

    def obter_total_produtos(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM produto")
            total_produtos = cursor.fetchone()[0]
            cursor.close()
            return total_produtos
        except Exception as e:
            print(f"Erro ao obter total de produtos: {e}")
            return 0

    def obter_produtos_baixo_estoque(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM produto WHERE estoque < 5")
            produtos_baixo_estoque = cursor.fetchone()[0]
            cursor.close()
            return produtos_baixo_estoque
        except Exception as e:
            print(f"Erro ao obter produtos com baixo estoque: {e}")
            return 0

    def obter_vendas_mes_atual(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT SUM(valor_total)
                FROM venda
                WHERE strftime('%m', data_venda) = strftime('%m', 'now')
                AND strftime('%Y', data_venda) = strftime('%Y', 'now')
            """)
            vendas_mes_atual = cursor.fetchone()[0]
            cursor.close()
            return vendas_mes_atual if vendas_mes_atual else 0
        except Exception as e:
            print(f"Erro ao obter vendas do mês atual: {e}")
            return 0

    def atualizar_dados_tela_inicial(self):
        total_produtos = self.obter_total_produtos()
        produtos_baixo_estoque = self.obter_produtos_baixo_estoque()
        vendas_mes_atual = self.obter_vendas_mes_atual()

        self.telas['inicial'].atualizar_resumo_produtos(total_produtos, produtos_baixo_estoque)
        self.telas['inicial'].atualizar_resumo_vendas(vendas_mes_atual)

    def logout(self):
        self.destroy()
        # Opcional: pode-se reiniciar o app chamando main() novamente, se desejado

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            print("Conexão com o banco de dados encerrada.")

def main():
    inicializar_cargos()
    from telas.tela_login import iniciar_tela_login
    user = iniciar_tela_login()
    if user:
        app = SistemaVendas(user)
        app.mainloop()

if __name__ == "__main__":
    nome_arquivo_sql = "graal.db"
    if not validar_arquivo_sql(nome_arquivo_sql):
        sys.exit(1) 
    inicializar_banco()
    main()