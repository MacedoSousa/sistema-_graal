import tkinter as tk
from tkinter import ttk

class TelaInicial(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.card_bemvindo = ttk.LabelFrame(self, text="Bem-vindo ao Sistema Graal", bootstyle="primary", padding=18)
        self.card_bemvindo.pack(pady=18, padx=24, fill="x")
        self.label_titulo = ttk.Label(self.card_bemvindo, text="Painel de Controle", font=("Arial", 22, "bold"), bootstyle="primary")
        self.label_titulo.pack(pady=6)

        self.cards_resumo = ttk.Frame(self)
        self.cards_resumo.pack(pady=18, padx=24, fill="x")

        self.card_produtos = ttk.LabelFrame(self.cards_resumo, text="Produtos", bootstyle="info", padding=16)
        self.card_produtos.pack(side="left", expand=True, fill="both", padx=8)
        self.label_total_produtos = ttk.Label(self.card_produtos, text="Total de Produtos: 0", font=("Arial", 14, "bold"), bootstyle="info")
        self.label_total_produtos.pack(pady=4)
        self.label_produtos_baixo_estoque = ttk.Label(self.card_produtos, text="Produtos em Baixo Estoque: 0", font=("Arial", 12), bootstyle="warning")
        self.label_produtos_baixo_estoque.pack(pady=4)

        self.card_vendas = ttk.LabelFrame(self.cards_resumo, text="Vendas", bootstyle="success", padding=16)
        self.card_vendas.pack(side="left", expand=True, fill="both", padx=8)
        self.label_vendas_mes_atual = ttk.Label(self.card_vendas, text="Vendas no Mês Atual: R$ 0.00", font=("Arial", 14, "bold"), bootstyle="success")
        self.label_vendas_mes_atual.pack(pady=4)

        self._agendar_atualizacao()

    def _agendar_atualizacao(self):
        self.after(2000, self._atualizacao_periodica)

    def _atualizacao_periodica(self):
        if hasattr(self.master, 'atualizar_dados_tela_inicial'):
            self.master.atualizar_dados_tela_inicial()
        self._agendar_atualizacao()

    def atualizar_resumo_produtos(self, total_produtos, produtos_baixo_estoque):
        self.label_total_produtos.config(text=f"Total de Produtos: {total_produtos}")
        self.label_produtos_baixo_estoque.config(text=f"Produtos em Baixo Estoque: {produtos_baixo_estoque}")
        if produtos_baixo_estoque > 0:
            self.label_produtos_baixo_estoque.config(bootstyle="danger")
        else:
            self.label_produtos_baixo_estoque.config(bootstyle="success")

    def atualizar_resumo_vendas(self, vendas_mes_atual):
        self.label_vendas_mes_atual.config(text=f"Vendas no Mês Atual: R$ {vendas_mes_atual:.2f}")
