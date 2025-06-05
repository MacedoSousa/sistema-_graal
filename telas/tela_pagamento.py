import tkinter as tk
from tkinter import ttk, messagebox
from telas.constantes import get_cor
from servicos.servico_comandas import listar_comandas_detalhadas
from servicos.servico_funcionarios import listar_funcionarios
from servicos.servico_pagamento import registrar_pagamento

class TelaPagamento(tk.Frame):
    def __init__(self, master, atualizar_todas_listas=None):
        super().__init__(master, bg='#f6faff')
        self.atualizar_todas_listas = atualizar_todas_listas
        self.comandas = []
        self.comanda_selecionada = None
        self.funcionarios = listar_funcionarios()
        self.filtro_var = tk.StringVar()
        self.cpf_var = tk.StringVar()
        self.forma_pagamento_var = tk.StringVar()
        self.funcionario_var = tk.StringVar()
        self._criar_widgets()
        self.atualizar_lista_comandas()

    def _criar_widgets(self):
        cabecalho = tk.Frame(self, bg=get_cor("cabecalho"))
        cabecalho.pack(fill='x')
        tk.Label(cabecalho, text="Pagamentos", bg=get_cor("cabecalho"), fg="white", font=("Segoe UI", 16, "bold")).pack(side='left', padx=10, pady=10)
        filtro_frame = tk.Frame(self, bg='#f6faff')
        filtro_frame.pack(fill='x', padx=20, pady=(10, 0))
        tk.Label(filtro_frame, text="Buscar Comanda:", font=("Segoe UI", 12), bg='#f6faff').pack(side='left')
        tk.Entry(filtro_frame, textvariable=self.filtro_var, font=("Segoe UI", 12), width=18).pack(side='left', padx=8)
        tk.Button(filtro_frame, text="Filtrar", command=self.atualizar_lista_comandas, bg="#2563eb", fg="white", font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2").pack(side='left', padx=8)
        self.cards_frame = tk.Frame(self, bg='#f6faff')
        self.cards_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.detalhes_frame = tk.Frame(self, bg='#f6faff')
        self.detalhes_frame.pack(fill='x', padx=20, pady=(0, 10))

    def atualizar_lista_comandas(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        filtro = self.filtro_var.get().strip().lower()
        self.comandas = [c for c in listar_comandas_detalhadas() if filtro in str(c['id']).lower()]
        if not self.comandas:
            tk.Label(self.cards_frame, text="Nenhuma comanda aberta encontrada.", font=("Segoe UI", 12), bg='#f6faff', fg='#e53e3e').pack(pady=18)
            return
        for c in self.comandas:
            card = tk.Frame(self.cards_frame, bg='white', highlightbackground='#e3e8ee', highlightthickness=2, bd=0)
            card.pack(fill='x', pady=8, padx=0)
            card.bind('<Button-1>', lambda e, cid=c['id']: self.selecionar_comanda(cid))
            header = tk.Frame(card, bg='white')
            header.pack(fill='x', pady=(8, 0))
            tk.Label(header, text=f"Comanda #{c['id']}", font=("Segoe UI", 14, "bold"), bg='white', fg='#2563eb').pack(side='left', padx=(12, 0))
            tk.Label(header, text=f"Status: {c['status'].capitalize()}", font=("Segoe UI", 11), bg='white', fg='#6b7280').pack(side='left', padx=(18, 0))
            tk.Label(header, text=f"Total: R$ {c['total']:.2f}", font=("Segoe UI", 13, "bold"), bg='white', fg='#22c55e').pack(side='right', padx=(0, 18))
            produtos_frame = tk.Frame(card, bg='white')
            produtos_frame.pack(fill='x', padx=18, pady=(4, 0))
            if c['itens']:
                for item in c['itens']:
                    tk.Label(produtos_frame, text=f"- {item['produto_nome']} x{item['quantidade']} (R$ {item['preco_unitario']:.2f} un)", font=("Segoe UI", 11), bg='white', fg='#23272b').pack(anchor='w')
            else:
                tk.Label(produtos_frame, text="Nenhum produto adicionado", font=("Segoe UI", 11, "italic"), bg='white', fg='#6b7280').pack(anchor='w')
            btn_pagar = tk.Button(card, text="Pagar", bg="#22c55e", fg="white", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, cursor="hand2", command=lambda comanda=c: self.abrir_modal_pagamento(comanda))
            btn_pagar.pack(side='right', padx=18, pady=8, ipadx=10, ipady=4)
        self.comanda_selecionada = None
        self._mostrar_detalhes(None)

    def selecionar_comanda(self, comanda_id):
        comanda = next((c for c in self.comandas if c['id'] == comanda_id), None)
        self.comanda_selecionada = comanda
        self._mostrar_detalhes(comanda)

    def _mostrar_detalhes(self, comanda):
        for widget in self.detalhes_frame.winfo_children():
            widget.destroy()
        if not comanda:
            return
        tk.Label(self.detalhes_frame, text=f"Pagamento da Comanda #{comanda['id']}", font=("Segoe UI", 15, "bold"), bg='#f6faff', fg='#2563eb').pack(anchor='w', pady=(8, 2))
        frame_prod = tk.Frame(self.detalhes_frame, bg='#f6faff')
        frame_prod.pack(anchor='w', pady=(0, 6))
        for item in comanda['itens']:
            tk.Label(frame_prod, text=f"- {item['produto_nome']} x{item['quantidade']} (R$ {item['preco_unitario']:.2f} un)", font=("Segoe UI", 11), bg='#f6faff', fg='#23272b').pack(anchor='w')
        tk.Label(self.detalhes_frame, text=f"Total: R$ {comanda['total']:.2f}", font=("Segoe UI", 13, "bold"), bg='#f6faff', fg='#22c55e').pack(anchor='w', pady=(4, 8))
        tk.Button(self.detalhes_frame, text="Realizar Pagamento", command=lambda: self.abrir_modal_pagamento(comanda), bg="#22c55e", fg="white", font=("Segoe UI", 13, "bold"), relief=tk.FLAT, cursor="hand2").pack(anchor='w', pady=(10, 0), ipadx=12, ipady=6)

    def abrir_modal_pagamento(self, comanda):
        modal = tk.Toplevel(self)
        modal.title(f"Pagamento da Comanda #{comanda['id']}")
        modal.geometry("440x520")
        modal.configure(bg='#f6faff')
        modal.transient(self)
        modal.grab_set()

        card_comanda = tk.Frame(modal, bg='white', highlightbackground='#e3e8ee', highlightthickness=2, bd=0)
        card_comanda.pack(fill='x', padx=24, pady=(24, 12))
        tk.Label(card_comanda, text=f"Comanda #{comanda['id']}", font=("Segoe UI", 15, "bold"), bg='white', fg='#2563eb').pack(anchor='w', pady=(12, 2), padx=18)
        for item in comanda['itens']:
            tk.Label(card_comanda, text=f"- {item['produto_nome']} x{item['quantidade']} (R$ {item['preco_unitario']:.2f} un)", font=("Segoe UI", 11), bg='white', fg='#23272b').pack(anchor='w', padx=32)
        tk.Label(card_comanda, text=f"Total: R$ {comanda['total']:.2f}", font=("Segoe UI", 13, "bold"), bg='white', fg='#22c55e').pack(anchor='w', padx=18, pady=(8, 12))

        card_pagamento = tk.Frame(modal, bg='white', highlightbackground='#e3e8ee', highlightthickness=2, bd=0)
        card_pagamento.pack(fill='x', padx=24, pady=(0, 12))
        tk.Label(card_pagamento, text="Funcionário:", font=("Segoe UI", 11), bg='white').pack(anchor='w', padx=18, pady=(14, 0))
        funcionarios_nomes = [f["nome"] for f in self.funcionarios]
        funcionario_cb = ttk.Combobox(card_pagamento, values=funcionarios_nomes, textvariable=self.funcionario_var, font=("Segoe UI", 11), state="readonly")
        funcionario_cb.pack(anchor='w', padx=18, pady=(0, 8))
        funcionario_cb.set("Selecione o funcionário")
        tk.Label(card_pagamento, text="CPF do Cliente:", font=("Segoe UI", 11), bg='white').pack(anchor='w', padx=18, pady=(0, 0))
        entry_cpf = tk.Entry(card_pagamento, textvariable=self.cpf_var, font=("Segoe UI", 11), width=22)
        entry_cpf.pack(anchor='w', padx=18, pady=(0, 8))
        entry_cpf.insert(0, "Opcional")
        tk.Label(card_pagamento, text="Forma de Pagamento:", font=("Segoe UI", 11), bg='white').pack(anchor='w', padx=18, pady=(0, 0))
        formas_pagamento = ["Cartão Crédito", "Cartão Débito", "PIX", "Dinheiro"]
        forma_cb = ttk.Combobox(card_pagamento, values=formas_pagamento, textvariable=self.forma_pagamento_var, font=("Segoe UI", 11), state="readonly")
        forma_cb.pack(anchor='w', padx=18, pady=(0, 8))
        forma_cb.set("Selecione a forma de pagamento")
        valor_pago_var = tk.StringVar()
        troco_var = tk.StringVar()
        frame_valor_pago = tk.Frame(card_pagamento, bg='white')
        label_valor_pago = tk.Label(frame_valor_pago, text="Valor Pago:", font=("Segoe UI", 11), bg='white')
        entry_valor_pago = tk.Entry(frame_valor_pago, textvariable=valor_pago_var, font=("Segoe UI", 11), width=12)
        label_troco = tk.Label(card_pagamento, textvariable=troco_var, font=("Segoe UI", 11, "bold"), bg='white', fg='#2563eb')
        def on_forma_change(event=None):
            if self.forma_pagamento_var.get() == 'Dinheiro':
                frame_valor_pago.pack(anchor='w', padx=18, pady=(4, 0))
                label_valor_pago.pack(side='left')
                entry_valor_pago.pack(side='left', padx=(8,0))
                label_troco.pack(anchor='w', padx=18, pady=(2, 0))
            else:
                frame_valor_pago.pack_forget()
                label_troco.pack_forget()
                troco_var.set("")
        forma_cb.bind('<<ComboboxSelected>>', on_forma_change)
        def calcular_troco(*_):
            try:
                valor_pago = float(valor_pago_var.get().replace(',', '.'))
                total = float(comanda['total'])
                if valor_pago >= total:
                    troco = valor_pago - total
                    troco_var.set(f"Troco: R$ {troco:.2f}")
                else:
                    falta = total - valor_pago
                    troco_var.set(f"Falta: R$ {falta:.2f}")
            except Exception:
                troco_var.set("")
        valor_pago_var.trace_add('write', calcular_troco)
        def confirmar():
            funcionario = self.funcionario_var.get()
            cpf = self.cpf_var.get()
            forma = self.forma_pagamento_var.get()
            if not funcionario or funcionario == "Selecione o funcionário":
                messagebox.showerror("Erro", "Selecione o funcionário.", parent=modal)
                return
            if not forma or forma == "Selecione a forma de pagamento":
                messagebox.showerror("Erro", "Selecione a forma de pagamento.", parent=modal)
                return
            if forma == 'Dinheiro':
                try:
                    valor_pago = float(valor_pago_var.get().replace(',', '.'))
                except Exception:
                    messagebox.showerror("Erro", "Informe um valor pago válido.", parent=modal)
                    return
                total = float(comanda['total'])
                if valor_pago < total:
                    messagebox.showerror("Erro", "Valor insuficiente para pagamento.", parent=modal)
                    return
            try:
                from servicos.servico_pagamento import registrar_pagamento
                registrar_pagamento(comanda['id'], funcionario, comanda['total'], forma, cpf)
                messagebox.showinfo("Sucesso", "Pagamento realizado com sucesso!", parent=modal)
                modal.destroy()
                self.atualizar_lista_comandas()
                if self.atualizar_todas_listas:
                    self.atualizar_todas_listas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar pagamento: {e}", parent=modal)
        tk.Button(card_pagamento, text="Confirmar Pagamento", command=confirmar, bg="#22c55e", fg="white", font=("Segoe UI", 13, "bold"), relief=tk.FLAT, cursor="hand2").pack(anchor='w', padx=18, pady=(18, 0), ipadx=12, ipady=6)
        tk.Button(card_pagamento, text="Cancelar", command=modal.destroy, bg="#e3e8ee", fg="#23272b", font=("Segoe UI", 12), relief=tk.FLAT, cursor="hand2").pack(anchor='w', padx=18, pady=(8, 0), ipadx=8, ipady=4)
