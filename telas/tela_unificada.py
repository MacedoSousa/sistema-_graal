import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from telas.constantes import get_cor

class TelaUnificada(tk.Frame):
    def __init__(self, master=None, usuario_cargo=None):
        super().__init__(master, bg='#f6faff')
        self.usuario_cargo = usuario_cargo or 'gerente'
        self.sidebar = tk.Frame(self, bg='#e3e8ee', width=180)
        self.sidebar.pack(side='left', fill='y')
        usuario_cargo = getattr(self, 'usuario_cargo', 'gerente')
        logo_path = 'img/graal.jpg'
        if Image and ImageTk and logo_path:
            if hasattr(self.sidebar, 'logo_img'):
                logo_img = self.sidebar.logo_img
            else:
                img = Image.open(logo_path)
                img = img.resize((48, 48))
                logo_img = ImageTk.PhotoImage(img)
                self.sidebar.logo_img = logo_img
            tk.Label(self.sidebar, image=logo_img, bg='#e3e8ee').pack(pady=(18, 6))
        tk.Label(self.sidebar, text='GRAAL', font=("Segoe UI", 18, "bold"), bg='#e3e8ee', fg='#2563eb').pack(pady=(18, 6))
        tk.Label(self.sidebar, text='Menu', font=("Segoe UI", 16, "bold"), bg='#e3e8ee', fg='#2563eb').pack(pady=(8, 8), padx=0)
        botoes = [
            ("Dashboard", self.abrir_dashboard),
            ("Comandas", self.abrir_comandas),
            ("Produtos", self.abrir_produtos),
            ("Funcionários", self.abrir_funcionarios),
            ("Pagamentos", self.abrir_pagamentos),
            ("Recibos", self.abrir_recibos),
        ]
        for nome, comando in botoes:
            tk.Button(
                self.sidebar,
                text=nome,
                command=comando,
                font=("Segoe UI", 13),
                bg='#e3e8ee',
                fg='#23272b',
                activebackground='#2563eb',
                activeforeground='white',
                relief=tk.FLAT,
                cursor="hand2"
            ).pack(fill='x', padx=12, pady=4)
        self.area_cards = tk.Frame(self, bg='#f6faff')
        self.area_cards.pack(side='left', fill='both', expand=True, padx=(0, 0), pady=(24, 0))
        card = tk.Frame(self.area_cards, bg='#f6faff')
        card.pack(fill='both', expand=True)
        total_produtos = 0
        vendas_mes = 0
        cards_info = [
            {"titulo": "Total em Estoque", "valor": total_produtos, "icone": "📦", "cor": '#2563eb', "legenda": "itens disponíveis"},
            {"titulo": "Vendas do Mês", "valor": f"R$ {vendas_mes:,.2f}", "icone": "📈", "cor": '#22c55e', "legenda": "faturamento mensal"},
        ]
        for idx, info in enumerate(cards_info):
            c = tk.Frame(card, bg='white', highlightbackground='#e3e8ee', highlightthickness=2, bd=0)
            c.grid(row=0, column=idx, padx=16, pady=16, sticky='n')
            tk.Label(c, text=info["icone"], font=("Segoe UI Emoji", 32), bg='white').pack(pady=(8, 0))
            tk.Label(c, text=info["titulo"], font=("Segoe UI", 13, "bold"), bg='white', fg=info["cor"]).pack(pady=(8, 0))
            tk.Label(c, text=info["valor"], font=("Segoe UI", 18, "bold"), bg='white', fg=info["cor"]).pack(pady=(0, 0))
            tk.Label(c, text=info["legenda"], font=("Segoe UI", 10), bg='white', fg='#6b7280').pack(pady=(0, 8))

    def limpar_area(self):
        for widget in self.area_cards.winfo_children():
            widget.destroy()

    def abrir_dashboard(self):
        from servicos.servico_produtos import obter_total_de_produtos
        from servicos.servico_vendas import obter_vendas_do_mes
        from servicos.servico_funcionarios import listar_funcionarios
        from servicos.servico_comandas import listar_comandas_detalhadas
        self.limpar_area()
        card = tk.Frame(self.area_cards, bg='#f6faff')
        card.pack(fill='both', expand=True)
        total_produtos = obter_total_de_produtos()
        vendas_mes = obter_vendas_do_mes()
        total_funcionarios = len(listar_funcionarios())
        comandas_abertas = len([c for c in listar_comandas_detalhadas() if c['status'] == 'aberta'])
        cards_info = [
            {"titulo": "Total em Estoque", "valor": total_produtos, "icone": "📦", "cor": '#2563eb', "legenda": "itens disponíveis"},
            {"titulo": "Vendas do Mês", "valor": f"R$ {vendas_mes:,.2f}", "icone": "📈", "cor": '#22c55e', "legenda": "faturamento mensal"},
            {"titulo": "Funcionários", "valor": total_funcionarios, "icone": "👥", "cor": '#a21caf', "legenda": "funcionários cadastrados"},
            {"titulo": "Comandas Abertas", "valor": comandas_abertas, "icone": "💳", "cor": '#ea580c', "legenda": "pendentes de pagamento"},
        ]
        for idx, info in enumerate(cards_info):
            c = tk.Frame(card, bg='white', highlightbackground=info["cor"], highlightthickness=2, bd=0)
            c.grid(row=0, column=idx, padx=(0 if idx == 0 else 8), pady=24, sticky='n')
            tk.Label(c, text=info["icone"], font=("Segoe UI Emoji", 32), bg='white').pack(pady=(8, 0))
            tk.Label(c, text=info["titulo"], font=("Segoe UI", 13, "bold"), bg='white', fg=info["cor"]).pack(pady=(8, 0))
            tk.Label(c, text=info["valor"], font=("Segoe UI", 18, "bold"), bg='white', fg=info["cor"]).pack(pady=(0, 0))
            tk.Label(c, text=info["legenda"], font=("Segoe UI", 10), bg='white', fg='#6b7280').pack(pady=(0, 8))

    def abrir_comandas(self):
        from telas.tela_comandas import TelaComandas
        self.limpar_area()
        TelaComandas(self.area_cards).pack(fill='both', expand=True)

    def abrir_produtos(self):
        from telas.tela_produtos import TelaProdutos
        self.limpar_area()
        TelaProdutos(self.area_cards).pack(fill='both', expand=True)

    def abrir_funcionarios(self):
        from telas.tela_funcionarios import TelaFuncionarios
        self.limpar_area()
        TelaFuncionarios(self.area_cards).pack(fill='both', expand=True)

    def abrir_pagamentos(self):
        from telas.tela_pagamento import TelaPagamento
        self.limpar_area()
        TelaPagamento(self.area_cards).pack(fill='both', expand=True)

    def abrir_recibos(self):
        from telas.tela_recibo import TelaRecibo
        self.limpar_area()
        TelaRecibo(self.area_cards).pack(fill='both', expand=True)

    # Inicializa com dashboard
    def _inicializar_dashboard(self):
        self.abrir_dashboard()

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self._inicializar_dashboard()

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self._inicializar_dashboard()

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self._inicializar_dashboard()
