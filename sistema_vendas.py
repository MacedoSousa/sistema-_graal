import tkinter as tk
from telas.tela_unificada import TelaUnificada
from servicos.database import conectar_banco_de_dados, inicializar_banco
from servicos.servico_funcionarios import inicializar_cargos
import os
import sys
from telas.constantes import criar_botao_tema, get_cor

def validar_arquivo_sql(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        print(f"Erro: O arquivo de banco '{nome_arquivo}' não existe.")
        return False
    if not nome_arquivo.lower().endswith(".db"):
        print(f"Erro: O arquivo '{nome_arquivo}' não é um banco SQLite válido.")
        return False
    return True

class SistemaVendas(tk.Tk):
    def __init__(self, usuario_logado):
        super().__init__() 
        self.protocol("WM_DELETE_WINDOW", self.sair)

        try:
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "img", "graal.ico")
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Não foi possível definir o ícone: {e}")

        self.title("Graal")
        self.geometry("1320x720")
        self.resizable(True, True)
        self.usuario_logado = usuario_logado
        self.configure(bg="#23272b") 

        self.conn = conectar_banco_de_dados()
        if self.conn is None:
            print("Não foi possível conectar ao banco de dados. O sistema será encerrado.")
            self.destroy()
            return

        self.header = tk.Frame(self, height=56, bg='white', highlightthickness=1, highlightbackground='#e3e8ee')
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        header_inner = tk.Frame(self.header, bg='white')
        header_inner.pack(fill="both", expand=True)

        tk.Label(header_inner, text="Graal - Sistema de Vendas", font=("Segoe UI", 18, "bold"), bg='white', fg='#23272b').pack(side="left", padx=32)

        self.btn_tema = criar_botao_tema(header_inner, callback=self.atualizar_tema)
        self.btn_tema.pack(side="right", padx=(0, 8), pady=0)

        usuario = self.usuario_logado.get('nome', 'Usuário')
        usuario_email = self.usuario_logado.get('email', '')
        from telas.constantes import criar_menu_usuario
        self.avatar_btn = criar_menu_usuario(
            header_inner,
            usuario,
            usuario_email,
            logout_callback=self.logout,
            sair_callback=self.sair
        )

        self.main_frame = tk.Frame(self, bg='white')
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.tela_unificada = TelaUnificada(self.main_frame, self.conn)
        self.tela_unificada.pack(fill="both", expand=True)

    def navegar_para_card(self, nome):
        self.menu_ativo.set(nome)
        if hasattr(self, 'tela_unificada') and nome in self.tela_unificada.cards:
            self.tela_unificada.mostrar_card(nome)
        for item in self.menu_itens:
            cor = '#2563eb' if item["nome"] == nome else '#6b7280'
            item['btn'].config(fg=cor)

    def atualizar_dados_tela_unificada(self):
        try:
            total_produtos = self.obter_total_produtos()
            self.tela_unificada.label_total_produtos.config(text=f"Total de Produtos: {total_produtos}")

        except Exception as e:
            print(f"Erro ao atualizar dados na tela unificada: {e}")

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
        from servicos.servico_funcionarios import listar_funcionarios
        total_funcionarios = len(listar_funcionarios())
        self.telas['inicial'].atualizar_resumo_produtos(total_produtos, produtos_baixo_estoque)
        self.telas['inicial'].atualizar_resumo_vendas(vendas_mes_atual)
        self.telas['inicial'].atualizar_resumo_funcionarios(total_funcionarios)

    def atualizar_todas_telas(self):
        if 'comandas' in self.telas:
            self.telas['comandas'].atualizar_listagem_comandas()
        if 'recibo' in self.telas:
            self.telas['recibo'].carregar_comandas_fechadas()
        if 'produtos' in self.telas:
            self.telas['produtos'].carregar_produtos()
        if 'funcionarios' in self.telas:
            self.telas['funcionarios'].atualizar_listagem_funcionarios()
        if 'inicial' in self.telas:
            self.atualizar_dados_tela_inicial()

    def atualizar_comandas_e_recibo(self):
        if 'comandas' in self.telas:
            self.telas['comandas'].atualizar_listagem_comandas()
        if 'recibo' in self.telas:
            self.telas['recibo'].carregar_comandas_fechadas()
        if 'inicial' in self.telas:
            self.atualizar_dados_tela_inicial()

    def atualizar_produtos_e_inicial(self):
        if 'produtos' in self.telas:
            self.telas['produtos'].carregar_produtos()
        if 'inicial' in self.telas:
            self.atualizar_dados_tela_inicial()

    def atualizar_funcionarios_e_inicial(self):
        if 'funcionarios' in self.telas:
            self.telas['funcionarios'].atualizar_listagem_funcionarios()
        if 'inicial' in self.telas:
            self.atualizar_dados_tela_inicial()

    def logout(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        root = tk.Tk()
        root.withdraw()
        self.destroy()
        from telas.tela_login import iniciar_tela_login
        from tkinter import messagebox
        messagebox.showinfo("Logout", "Sessão encerrada com sucesso.")
        user = iniciar_tela_login()
        if user:
            app = SistemaVendas(user)
            app.mainloop()

    def sair(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        self.destroy()
        import os
        os._exit(0)

    def atualizar_tema(self):
        self.configure(bg=get_cor('fundo_janela'))
        if hasattr(self, 'tela_unificada') and hasattr(self.tela_unificada, 'on_show'):
            self.tela_unificada.on_show()

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
    from telas.tela_login import iniciar_tela_login
    user = iniciar_tela_login()
    if user:
        app = SistemaVendas(user)
        app.mainloop()