import tkinter as tk
from tkinter import ttk, messagebox
from telas.constantes import get_cor
from servicos.servico_produtos import listar_produtos, salvar_produto, excluir_produto
from servicos.servico_funcionarios import listar_funcionarios, cadastrar_funcionario
from servicos.servico_comandas import listar_comandas, abrir_nova_comanda
from servicos.servico_pagamento import registrar_pagamento
from servicos.servico_recibo import listar_recibos

class TelaUnificada(tk.Frame):
    def __init__(self, container, conn):
        super().__init__(container, bg='white')
        self.conn = conn
        self.pack(fill='both', expand=True)
        self.cards = {}
        self.criar_menu()
        self.criar_area_cards()
        self.mostrar_card('Dashboard')

    def criar_menu(self):
        menu = tk.Frame(self, bg='white')
        menu.pack(pady=32)
        botoes = [
            ('Dashboard', lambda: self.mostrar_card('Dashboard')),
            ('Produtos', lambda: self.mostrar_card('Produtos')),
            ('Funcionários', lambda: self.mostrar_card('Funcionários')),
            ('Comandas', lambda: self.mostrar_card('Comandas')),
            ('Pagamentos', lambda: self.mostrar_card('Pagamentos')),
            ('Recibos', lambda: self.mostrar_card('Recibos')),
        ]
        for nome, cmd in botoes:
            btn = tk.Button(menu, text=nome, font=("Arial", 12, "bold"), bg=get_cor('botao_bg'), fg=get_cor('botao_fg'), relief="flat", bd=0, padx=18, pady=8, cursor="hand2", command=cmd)
            btn.pack(side='left', padx=12)

    def criar_area_cards(self):
        self.area_cards = tk.Frame(self, bg='white')
        self.area_cards.pack(expand=True)
        self.cards['Dashboard'] = self.criar_card_dashboard()
        self.cards['Produtos'] = self.criar_card_produtos()
        self.cards['Funcionários'] = self.criar_card_funcionarios()
        self.cards['Comandas'] = self.criar_card_comandas()
        self.cards['Pagamentos'] = self.criar_card_pagamentos()
        self.cards['Recibos'] = self.criar_card_recibos()

    def mostrar_card(self, nome):
        for card in self.cards.values():
            card.pack_forget()
        self.cards[nome].pack(expand=True)

    def criar_card_dashboard(self):
        card = tk.Frame(self.area_cards, bg='white', highlightthickness=0)
        tk.Label(card, text="Dashboard", font=("Arial Black", 26, "bold"), bg='white', fg=get_cor('texto_label')).pack(pady=(32, 16))
        # Centralização elegante
        frame_center = tk.Frame(card, bg='white')
        frame_center.pack(expand=True)
        # Funções auxiliares para buscar dados
        try:
            total_produtos = len(listar_produtos())
        except Exception:
            total_produtos = 0
        try:
            baixo_estoque = sum(1 for p in listar_produtos() if p.get('quantidade', 0) < 5)
        except Exception:
            baixo_estoque = 0
        try:
            total_funcionarios = len(listar_funcionarios())
        except Exception:
            total_funcionarios = 0
        try:
            from servicos.servico_vendas import obter_vendas_mes_atual
            vendas_mes = obter_vendas_mes_atual()
        except Exception:
            vendas_mes = 0
        try:
            total_comandas = len(listar_comandas())
        except Exception:
            total_comandas = 0
        try:
            total_recibos = len(listar_recibos())
        except Exception:
            total_recibos = 0
        # Cards com ícones, sombra e borda arredondada
        cards_info = [
            ("📦 Produtos", total_produtos, '#2563eb'),
            ("⚠️ Baixo Estoque", baixo_estoque, '#eab308' if baixo_estoque > 0 else '#22c55e'),
            ("👥 Funcionários", total_funcionarios, '#a21caf'),
            ("💰 Vendas do Mês", vendas_mes, '#22c55e'),
            ("🛒 Comandas Abertas", total_comandas, '#f59e42'),
            ("🧾 Recibos", total_recibos, '#2563eb'),
        ]
        cards_frame = tk.Frame(frame_center, bg='white')
        cards_frame.grid(row=0, column=0, pady=24)
        for i, (titulo, valor, cor) in enumerate(cards_info):
            c = tk.Frame(cards_frame, bg='white', highlightthickness=0, bd=0)
            c.grid(row=i//3, column=i%3, padx=32, pady=24, ipadx=12, ipady=12, sticky='nsew')
            # Sombra
            sombra = tk.Frame(c, bg='#e3e8ee', width=180, height=120)
            sombra.place(x=8, y=8)
            # Card principal
            card_main = tk.Frame(c, bg='white', highlightthickness=0, bd=0)
            card_main.place(x=0, y=0)
            card_main.configure(width=180, height=120)
            card_main.pack_propagate(False)
            card_main.config(highlightbackground=cor, highlightcolor=cor, highlightthickness=2)
            card_main.config(borderwidth=0)
            # Conteúdo
            tk.Label(card_main, text=titulo, font=("Arial", 14, "bold"), bg='white', fg=cor).pack(pady=(18,0))
            tk.Label(card_main, text=str(valor), font=("Arial Black", 28, "bold"), bg='white', fg='#23272b').pack(pady=(0,10))
        # Centralizar grid
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)
        return card

    def criar_card_produtos(self):
        card = tk.Frame(self.area_cards, bg='white', highlightthickness=1, highlightbackground='#e3e8ee')
        tk.Label(card, text="Produtos", font=("Arial Black", 18, "bold"), bg='white', fg=get_cor('texto_label')).pack(pady=18)
        self.lista_produtos = tk.Listbox(card, font=("Arial", 11), width=60, height=10)
        self.lista_produtos.pack(pady=8)
        self.atualizar_lista_produtos()
        btn_add = tk.Button(card, text="Adicionar Produto", command=self.abrir_modal_produto, font=("Arial", 11), bg=get_cor('botao_bg'), fg=get_cor('botao_fg'))
        btn_add.pack(pady=8)
        return card

    def atualizar_lista_produtos(self):
        self.lista_produtos.delete(0, tk.END)
        for p in listar_produtos():
            self.lista_produtos.insert(tk.END, f"{p['nome']} | Estoque: {p['quantidade']}")

    def abrir_modal_produto(self):
        win = tk.Toplevel(self)
        win.title("Novo Produto")
        win.geometry("400x300")
        nome = tk.Entry(win, font=("Arial", 11))
        nome.pack(pady=8)
        tk.Label(win, text="Nome").pack()
        estoque = tk.Entry(win, font=("Arial", 11))
        estoque.pack(pady=8)
        tk.Label(win, text="Estoque").pack()
        def salvar():
            salvar_produto({'nome': nome.get(), 'quantidade': int(estoque.get())})
            self.atualizar_lista_produtos()
            win.destroy()
        tk.Button(win, text="Salvar", command=salvar).pack(pady=12)

    def criar_card_funcionarios(self):
        card = tk.Frame(self.area_cards, bg='white', highlightthickness=1, highlightbackground='#e3e8ee')
        tk.Label(card, text="Funcionários", font=("Arial Black", 18, "bold"), bg='white', fg=get_cor('texto_label')).pack(pady=18)
        self.lista_funcionarios = tk.Listbox(card, font=("Arial", 11), width=60, height=10)
        self.lista_funcionarios.pack(pady=8)
        self.atualizar_lista_funcionarios()
        btn_add = tk.Button(card, text="Adicionar Funcionário", command=self.abrir_modal_funcionario, font=("Arial", 11), bg=get_cor('botao_bg'), fg=get_cor('botao_fg'))
        btn_add.pack(pady=8)
        return card

    def atualizar_lista_funcionarios(self):
        self.lista_funcionarios.delete(0, tk.END)
        for f in listar_funcionarios():
            self.lista_funcionarios.insert(tk.END, f"{f['nome']} | {f['cargo']}")

    def abrir_modal_funcionario(self):
        win = tk.Toplevel(self)
        win.title("Novo Funcionário")
        win.geometry("400x300")
        nome = tk.Entry(win, font=("Arial", 11))
        nome.pack(pady=8)
        tk.Label(win, text="Nome").pack()
        cargo = tk.Entry(win, font=("Arial", 11))
        cargo.pack(pady=8)
        tk.Label(win, text="Cargo").pack()
        def salvar():
            cadastrar_funcionario({'nome': nome.get(), 'cargo': cargo.get()})
            self.atualizar_lista_funcionarios()
            win.destroy()
        tk.Button(win, text="Salvar", command=salvar).pack(pady=12)

    def criar_card_comandas(self):
        card = tk.Frame(self.area_cards, bg='white', highlightthickness=1, highlightbackground='#e3e8ee')
        tk.Label(card, text="Comandas", font=("Arial Black", 18, "bold"), bg='white', fg=get_cor('texto_label')).pack(pady=18)
        self.lista_comandas = tk.Listbox(card, font=("Arial", 11), width=60, height=10)
        self.lista_comandas.pack(pady=8)
        self.atualizar_lista_comandas()
        btn_add = tk.Button(card, text="Abrir Comanda", command=self.abrir_modal_comanda, font=("Arial", 11), bg=get_cor('botao_bg'), fg=get_cor('botao_fg'))
        btn_add.pack(pady=8)
        return card

    def atualizar_lista_comandas(self):
        self.lista_comandas.delete(0, tk.END)
        for c in listar_comandas():
            self.lista_comandas.insert(tk.END, f"Comanda {c['id']} | {c['status']}")

    def abrir_modal_comanda(self):
        win = tk.Toplevel(self)
        win.title("Nova Comanda")
        win.geometry("400x200")
        funcionario = tk.Entry(win, font=("Arial", 11))
        funcionario.pack(pady=8)
        tk.Label(win, text="Funcionário").pack()
        def salvar():
            abrir_nova_comanda({'funcionario': funcionario.get()})
            self.atualizar_lista_comandas()
            win.destroy()
        tk.Button(win, text="Abrir", command=salvar).pack(pady=12)

    def criar_card_pagamentos(self):
        card = tk.Frame(self.area_cards, bg='white', highlightthickness=1, highlightbackground='#e3e8ee')
        tk.Label(card, text="Pagamentos", font=("Arial Black", 18, "bold"), bg='white', fg=get_cor('texto_label')).pack(pady=18)
        # Exemplo simples
        tk.Label(card, text="Funcionalidade de pagamento aqui", bg='white').pack(pady=24)
        return card

    def criar_card_recibos(self):
        card = tk.Frame(self.area_cards, bg='white', highlightthickness=1, highlightbackground='#e3e8ee')
        tk.Label(card, text="Recibos", font=("Arial Black", 18, "bold"), bg='white', fg=get_cor('texto_label')).pack(pady=18)
        self.lista_recibos = tk.Listbox(card, font=("Arial", 11), width=60, height=10)
        self.lista_recibos.pack(pady=8)
        self.atualizar_lista_recibos()
        return card

    def atualizar_lista_recibos(self):
        self.lista_recibos.delete(0, tk.END)
        for r in listar_recibos():
            self.lista_recibos.insert(tk.END, f"Recibo {r['id']} | Valor: {r['valor']}")
