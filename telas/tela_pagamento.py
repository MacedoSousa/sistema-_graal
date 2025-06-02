import tkinter as tk
from tkinter import ttk, messagebox
from telas.tela_base import TelaBase
from servicos.servico_pagamento import registrar_pagamento
from servicos.servico_comandas import obter_comanda, fechar_comanda
from servicos.utils import validar_cpf, campo_obrigatorio, logar_erro

class TelaPagamento(TelaBase):
    def __init__(self, container, conn):
        super().__init__(container, title="")
        self.conn = conn
        self.numero_comanda = None
        self.comanda = None
        self.valor_total = 0.0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        frame_comanda = ttk.LabelFrame(self, text="Selecione a Comanda para Pagamento", bootstyle="primary", padding=15)
        frame_comanda.grid(row=0, column=0, padx=30, pady=18, sticky="ew")
        ttk.Label(frame_comanda, text="Número da Comanda:", font=("Arial", 12, "bold"), bootstyle="primary").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.comanda_entry = ttk.Entry(frame_comanda, font=("Arial", 12), width=12)
        self.comanda_entry.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        ttk.Button(frame_comanda, text="Buscar", bootstyle="info", command=self.buscar_comanda).grid(row=0, column=2, padx=8, pady=8)

        self.frame_itens = ttk.LabelFrame(self, text="Itens da Comanda", bootstyle="info", padding=15)
        self.frame_itens.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.frame_itens.grid_columnconfigure(0, weight=1)
        self.treeview_itens = ttk.Treeview(self.frame_itens, columns=("Nome", "Quantidade", "Preço Unitário", "Subtotal"), show="headings", height=7)
        self.treeview_itens.heading("Nome", text="Nome")
        self.treeview_itens.heading("Quantidade", text="Quantidade")
        self.treeview_itens.heading("Preço Unitário", text="Preço Unitário (R$)")
        self.treeview_itens.heading("Subtotal", text="Subtotal (R$)")
        self.treeview_itens.column("Nome", width=150)
        self.treeview_itens.column("Quantidade", width=100)
        self.treeview_itens.column("Preço Unitário", width=120)
        self.treeview_itens.column("Subtotal", width=120)
        self.treeview_itens.pack(fill="both", expand=True)

        self.frame_pagamento = ttk.LabelFrame(self, text="Pagamento", bootstyle="success", padding=20)
        self.frame_pagamento.grid(row=2, column=0, padx=30, pady=18, sticky="ew")
        self.frame_pagamento.grid_columnconfigure(0, weight=1)
        self.frame_pagamento.grid_columnconfigure(1, weight=1)

        ttk.Label(self.frame_pagamento, text="CPF do Cliente:", font=("Arial", 12, "bold"), bootstyle="primary").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.cpf_entry = ttk.Entry(self.frame_pagamento, font=("Arial", 12))
        self.cpf_entry.grid(row=0, column=1, padx=5, pady=8, sticky="ew")

        ttk.Label(self.frame_pagamento, text="Forma de Pagamento:", font=("Arial", 12, "bold"), bootstyle="primary").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.pagamento_combobox = ttk.Combobox(self.frame_pagamento,
                                               values=["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix"],
                                               font=("Arial", 12),
                                               state="readonly")
        self.pagamento_combobox.grid(row=1, column=1, padx=5, pady=8, sticky="ew")
        self.pagamento_combobox.current(0)

        self.label_total = ttk.Label(self.frame_pagamento, text="Total: R$ 0.00", font=("Arial", 16, "bold"), bootstyle="success")
        self.label_total.grid(row=2, column=0, columnspan=2, pady=10, sticky="e")

        self.finalizar_button = ttk.Button(self.frame_pagamento, text="Finalizar Pagamento", bootstyle="warning",
                                           command=self.finalizar_pagamento, width=22)
        self.finalizar_button.grid(row=3, column=0, columnspan=2, pady=18)
        self.finalizar_button.config(state="disabled")

    def buscar_comanda(self):
        numero = self.comanda_entry.get().strip()
        if not numero.isdigit():
            messagebox.showerror("Erro", "Digite um número de comanda válido.")
            return
        comanda = obter_comanda(int(numero))
        if not comanda:
            messagebox.showerror("Erro", f"Comanda {numero} não encontrada ou sem itens.")
            self.limpar_itens()
            return
        self.numero_comanda = int(numero)
        self.comanda = comanda
        self.atualizar_itens_comanda()
        self.finalizar_button.config(state="normal")

    def atualizar_itens_comanda(self):
        self.treeview_itens.delete(*self.treeview_itens.get_children())
        total = 0.0
        for item in self.comanda['itens']:
            subtotal = item['preco_unitario'] * item['quantidade']
            self.treeview_itens.insert("", "end", values=(
                item['produto_nome'],
                item['quantidade'],
                f"{item['preco_unitario']:.2f}",
                f"{subtotal:.2f}"
            ))
            total += subtotal
        self.valor_total = total
        self.label_total.config(text=f"Total: R$ {self.valor_total:.2f}")

    def limpar_itens(self):
        self.treeview_itens.delete(*self.treeview_itens.get_children())
        self.label_total.config(text="Total: R$ 0.00")
        self.finalizar_button.config(state="disabled")
        self.comanda = None
        self.numero_comanda = None

    def finalizar_pagamento(self):
        if not self.comanda or not self.comanda['itens']:
            messagebox.showerror("Erro", "Nenhuma comanda carregada.")
            return

        cpf_cliente = self.cpf_entry.get().strip()
        forma_pagamento = self.pagamento_combobox.get()

        if cpf_cliente and not validar_cpf(cpf_cliente):
            messagebox.showerror("Erro", "CPF inválido. Digite 11 números.")
            return

        if not campo_obrigatorio(forma_pagamento):
            messagebox.showerror("Erro", "Selecione a forma de pagamento.")
            return

        if not messagebox.askyesno("Confirmar", "Deseja finalizar o pagamento?"):
            return

        try:
            id_pedido = self.numero_comanda
            registrar_pagamento(id_pedido, cpf_cliente, self.valor_total, forma_pagamento)
            fechar_comanda(id_pedido)

            if hasattr(self.master, 'tela_recibo'):
                produtos = [
                    {
                        'nome': item['produto_nome'],
                        'quantidade': item['quantidade'],
                        'preco': item['preco_unitario']
                    } for item in self.comanda['itens']
                ]
                self.master.tela_recibo.exibir_recibo(id_pedido, cpf_cliente, produtos, self.valor_total, forma_pagamento)
                self.master.mostrar_tela('recibo')

            messagebox.showinfo("Sucesso", "Pagamento realizado e recibo gerado!")

            self.limpar_itens()
            self.comanda_entry.delete(0, tk.END)
            self.cpf_entry.delete(0, tk.END)
            self.pagamento_combobox.current(0)

            if hasattr(self.master, 'telas') and 'comandas' in self.master.telas:
                self.master.telas['comandas'].atualizar_listagem_comandas()

        except Exception as e:
            logar_erro(e)
            messagebox.showerror("Erro", f"Erro ao finalizar pagamento: {e}")
