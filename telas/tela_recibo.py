import tkinter as tk
from tkinter import ttk, messagebox
from telas.constantes import get_cor
from servicos.servico_recibo import listar_recibos
import os
from datetime import datetime

class TelaRecibo(tk.Frame):
    def __init__(self, master, atualizar_todas_listas=None):
        super().__init__(master, bg='#f6faff')
        self.atualizar_todas_listas = atualizar_todas_listas
        self.recibos_feedback_var = tk.StringVar()
        self.recibos_feedback_label = tk.Label(self, textvariable=self.recibos_feedback_var, font=("Segoe UI", 11, "bold"), bg='#f6faff', fg='#e53e3e')
        self.recibos_feedback_label.pack(fill='x', padx=32, pady=(8, 0))
        self.recibos_feedback_label.pack_forget()
        self.criar_cards_recibos()

    def criar_cards_recibos(self):
        cabecalho_frame = tk.Frame(self, bg=get_cor("cabecalho"))
        cabecalho_frame.pack(fill='x')
        titulo = tk.Label(cabecalho_frame, text="Recibos", bg=get_cor("cabecalho"), fg="white", font=("Segoe UI", 16, "bold"))
        titulo.pack(side='left', padx=10, pady=10)
        container = tk.Frame(self, bg='#f6faff')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        canvas = tk.Canvas(container, bg='#f6faff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.cards_frame = tk.Frame(canvas, bg='#f6faff')
        self.cards_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.atualizar_lista_recibos()

    def atualizar_lista_recibos(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        recibos = listar_recibos()
        if not recibos:
            self.recibos_feedback_var.set("Nenhum recibo encontrado.")
            self.recibos_feedback_label.pack(fill='x', padx=32, pady=(8, 0))
        else:
            self.recibos_feedback_label.pack_forget()
        max_por_linha = 2
        for idx, r in enumerate(recibos):
            row = idx // max_por_linha
            col = idx % max_por_linha
            self.criar_card_recibo(r, row, col)

    def criar_card_recibo(self, recibo, row=0, col=0):
        card = tk.Frame(
            self.cards_frame,
            bg='white',
            highlightbackground='#d1d5db',
            highlightthickness=2,
            bd=0,
        )
        card.grid(row=row, column=col, padx=24, pady=18, sticky='n')
        card.configure(relief='raised')
        sombra = tk.Frame(self.cards_frame, bg='#e3e8ee', width=320, height=180)
        sombra.grid(row=row, column=col, padx=28, pady=22, sticky='n')
        sombra.lower(card)
        header = tk.Frame(card, bg='white')
        header.pack(fill='x', pady=(8, 0))
        tk.Label(header, text=f"Recibo #{recibo.get('id_pedido','-')}", font=("Segoe UI", 14, "bold"), bg='white', fg='#2563eb').pack(side='left', padx=(0, 8))
        valor_total = recibo.get('valor_total', 0)
        try:
            valor_total = float(valor_total)
        except Exception:
            valor_total = 0.0
        tk.Label(header, text=f"R$ {valor_total:.2f}", font=("Segoe UI", 13, "bold"), bg='white', fg='#22c55e').pack(side='right', padx=(8, 0))
        tk.Frame(card, bg='#e3e8ee', height=2).pack(fill='x', padx=8, pady=(6, 6))
        info = tk.Frame(card, bg='white')
        info.pack(fill='x', pady=(0, 0))
        tk.Label(info, text=f"Data:", font=("Segoe UI", 10, "bold"), bg='white', fg='#6b7280').grid(row=0, column=0, sticky='w')
        tk.Label(info, text=recibo.get('data_venda', '-'), font=("Segoe UI", 11), bg='white', fg='#23272b').grid(row=0, column=1, sticky='w', padx=(4, 16))
        tk.Label(info, text=f"CPF Cliente:", font=("Segoe UI", 10, "bold"), bg='white', fg='#6b7280').grid(row=1, column=0, sticky='w')
        tk.Label(info, text=recibo.get('cpf_cliente', '-'), font=("Segoe UI", 11), bg='white', fg='#23272b').grid(row=1, column=1, sticky='w', padx=(4, 16))
        tk.Label(info, text=f"Pagamento:", font=("Segoe UI", 10, "bold"), bg='white', fg='#6b7280').grid(row=2, column=0, sticky='w')
        tk.Label(info, text=recibo.get('forma_pagamento', '-'), font=("Segoe UI", 11), bg='white', fg='#23272b').grid(row=2, column=1, sticky='w', padx=(4, 16))
        for i in range(4):
            info.grid_columnconfigure(i, weight=1)
        btn = tk.Button(
            card,
            text="Detalhes",
            command=lambda: self.abrir_modal_detalhes_recibo(recibo.get('id_pedido')),
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn.pack(pady=(12, 8), ipadx=10, ipady=5, anchor='e')

    def abrir_modal_detalhes_recibo(self, recibo_id):
        from servicos.servico_recibo import obter_dados_recibo
        dados = obter_dados_recibo(recibo_id)
        if not dados:
            messagebox.showerror("Erro", "Não foi possível obter os dados do recibo.")
            return
        modal = tk.Toplevel(self)
        modal.title(f"Recibo #{recibo_id}")
        modal.geometry("420x520")
        modal.configure(bg='white')
        modal.transient(self)
        modal.grab_set()
        card = tk.Frame(modal, bg='white', highlightbackground='#e3e8ee', highlightthickness=2, bd=0)
        card.pack(fill='both', expand=True, padx=24, pady=24)
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'graal.jpg')
        if os.path.exists(logo_path):
            from PIL import Image, ImageTk
            img = Image.open(logo_path)
            img = img.resize((56, 56))
            logo_img = ImageTk.PhotoImage(img)
            card.logo_img = logo_img
            tk.Label(card, image=logo_img, bg='white').pack(pady=(0, 8))
        tk.Label(card, text=f"Recibo #{recibo_id}", font=("Segoe UI", 16, "bold"), bg='white', fg='#2563eb').pack(pady=(0, 8))
        tk.Label(card, text=f"Funcionário: {dados.get('funcionario', '-')}", font=("Segoe UI", 12), bg='white').pack(anchor='w', padx=8)
        tk.Label(card, text=f"CPF Cliente: {dados.get('cpf_cliente', '-')}", font=("Segoe UI", 12), bg='white').pack(anchor='w', padx=8)
        tk.Label(card, text=f"Data da Compra: {dados.get('data_venda', '-')}", font=("Segoe UI", 12), bg='white').pack(anchor='w', padx=8)
        tk.Label(card, text=f"Forma de Pagamento: {dados.get('forma_pagamento', '-')}", font=("Segoe UI", 12), bg='white').pack(anchor='w', padx=8)
        tk.Label(card, text="Produtos:", font=("Segoe UI", 12, "bold"), bg='white').pack(anchor='w', padx=8, pady=(10, 0))
        for prod in dados['produtos']:
            tk.Label(card, text=f"- {prod['nome']} x{prod['quantidade']} (R$ {prod['preco']:.2f} un)", font=("Segoe UI", 11), bg='white').pack(anchor='w', padx=18)
        tk.Label(card, text=f"Total: R$ {dados.get('valor_total', 0):.2f}", font=("Segoe UI", 13, "bold"), bg='white', fg='#22c55e').pack(anchor='w', padx=8, pady=(10, 0))
        tk.Label(card, text=f"Impresso em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", font=("Segoe UI", 10), bg='white', fg='#6b7280').pack(anchor='w', padx=8, pady=(10, 0))
        def imprimir_pdf():
            messagebox.showinfo("PDF não disponível", "A exportação para PDF está desativada neste ambiente.", parent=modal)
        tk.Button(card, text="Imprimir PDF", command=imprimir_pdf, bg="#2563eb", fg="white", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, cursor="hand2").pack(pady=(18, 0), ipadx=10, ipady=6)
        tk.Button(card, text="Fechar", command=modal.destroy, bg="#e3e8ee", fg="#23272b", font=("Segoe UI", 12), relief=tk.FLAT, cursor="hand2").pack(pady=(8, 0), ipadx=8, ipady=4)
