from tkinter import ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from servicos.servico_recibo import gerar_recibo_dados, listar_comandas_fechadas, obter_dados_recibo
from telas.tela_base import TelaBase

class TelaRecibo(TelaBase):
    def __init__(self, container, conn):
        super().__init__(container, title="")
        self.conn = conn
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_listagem = ttk.LabelFrame(self, text="Comandas Fechadas", bootstyle="primary", padding=12)
        self.frame_listagem.grid(row=0, column=0, padx=30, pady=18, sticky="nsew")
        self.frame_listagem.grid_columnconfigure(0, weight=1)
        self.treeview_comandas = ttk.Treeview(self.frame_listagem, columns=("Numero", "Data", "Total", "CPF", "Pagamento"), show="headings", height=7)
        self.treeview_comandas.heading("Numero", text="Número")
        self.treeview_comandas.heading("Data", text="Data")
        self.treeview_comandas.heading("Total", text="Total (R$)")
        self.treeview_comandas.heading("CPF", text="CPF Cliente")
        self.treeview_comandas.heading("Pagamento", text="Pagamento")
        self.treeview_comandas.column("Numero", width=80, anchor="center")
        self.treeview_comandas.column("Data", width=140, anchor="center")
        self.treeview_comandas.column("Total", width=100, anchor="center")
        self.treeview_comandas.column("CPF", width=120, anchor="center")
        self.treeview_comandas.column("Pagamento", width=120, anchor="center")
        self.treeview_comandas.pack(fill="both", expand=True, padx=8, pady=8)
        self.treeview_comandas.bind("<Double-1>", self.abrir_recibo_comanda)
        self.carregar_comandas_fechadas()

        self.card = ttk.LabelFrame(self, text="Recibo de Compra", bootstyle="primary", padding=28)
        self.card.grid(row=1, column=0, padx=60, pady=30, sticky="nsew")
        self.card.grid_columnconfigure(0, weight=1)
        self.titulo_label = ttk.Label(self.card, text="Recibo de Compra", font=("Arial", 22, "bold"), bootstyle="primary")
        self.titulo_label.grid(row=0, column=0, pady=(0, 18), sticky="ew")
        self.data_label = ttk.Label(self.card, text="", font=("Arial", 13), bootstyle="secondary")
        self.data_label.grid(row=1, column=0, pady=2, sticky="w")
        self.pedido_label = ttk.Label(self.card, text="Pedido:", font=("Arial", 13, "bold"), bootstyle="info")
        self.pedido_label.grid(row=2, column=0, pady=2, sticky="w")
        self.cpf_label = ttk.Label(self.card, text="CPF Cliente:", font=("Arial", 13), bootstyle="info")
        self.cpf_label.grid(row=3, column=0, pady=2, sticky="w")
        self.produtos_label = ttk.Label(self.card, text="Produtos:", font=("Arial", 13, "bold"), bootstyle="primary")
        self.produtos_label.grid(row=4, column=0, pady=(12,2), sticky="w")
        self.lista_produtos_label = ttk.Label(self.card, text="", font=("Consolas", 12), bootstyle="secondary", justify="left", anchor="w")
        self.lista_produtos_label.grid(row=5, column=0, padx=10, pady=2, sticky="ew")
        self.sep = ttk.Separator(self.card, orient="horizontal")
        self.sep.grid(row=6, column=0, sticky="ew", pady=10)
        self.total_label = ttk.Label(self.card, text="Total:", font=("Arial", 16, "bold"), bootstyle="success")
        self.total_label.grid(row=7, column=0, pady=2, sticky="w")
        self.pagamento_label = ttk.Label(self.card, text="Pagamento:", font=("Arial", 13), bootstyle="info")
        self.pagamento_label.grid(row=8, column=0, pady=2, sticky="w")

    def carregar_comandas_fechadas(self):
        self.treeview_comandas.delete(*self.treeview_comandas.get_children())
        for comanda in listar_comandas_fechadas():
            self.treeview_comandas.insert("", "end", values=(comanda['id_pedido'], comanda['data_venda'], f"{comanda['valor_total']:.2f}", comanda['cpf_cliente'], comanda['forma_pagamento']))

    def abrir_recibo_comanda(self, event):
        selecionados = self.treeview_comandas.selection()
        if not selecionados:
            return
        item_id = selecionados[0]
        numero_comanda = self.treeview_comandas.item(item_id, 'values')[0]
        dados = obter_dados_recibo(numero_comanda)
        if not dados:
            return
        self.exibir_recibo(dados['id_pedido'], dados['cpf_cliente'], dados['produtos'], dados['valor_total'], dados['forma_pagamento'])

    def exibir_recibo(self, id_pedido, cpf_cliente, produtos, valor_total, forma_pagamento):
        recibo_dados = gerar_recibo_dados(id_pedido, cpf_cliente, produtos, valor_total, forma_pagamento)
        for widget in self.card.winfo_children():
            widget.destroy()
        self.card.grid_columnconfigure(0, weight=1)
        row = 0
        ttk.Label(self.card, text="GRAAL", font=("Arial", 22, "bold"), bootstyle="primary").grid(row=row, column=0, pady=(8, 2), sticky="ew")
        row += 1
        ttk.Label(self.card, text="Recibo de Venda", font=("Arial", 16, "bold"), bootstyle="info").grid(row=row, column=0, pady=(0, 10), sticky="ew")
        row += 1
        ttk.Separator(self.card, orient="horizontal").grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        row += 1
        ttk.Label(self.card, text=f"Data: {recibo_dados['data']}", font=("Arial", 12)).grid(row=row, column=0, sticky="w", padx=12)
        row += 1
        ttk.Label(self.card, text=f"Pedido: {recibo_dados['pedido']}", font=("Arial", 12)).grid(row=row, column=0, sticky="w", padx=12)
        row += 1
        if recibo_dados['cpf_cliente']:
            ttk.Label(self.card, text=f"CPF Cliente: {recibo_dados['cpf_cliente']}", font=("Arial", 12)).grid(row=row, column=0, sticky="w", padx=12)
            row += 1
        ttk.Label(self.card, text=f"Pagamento: {recibo_dados['pagamento']}", font=("Arial", 12)).grid(row=row, column=0, sticky="w", padx=12)
        row += 1
        ttk.Separator(self.card, orient="horizontal").grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        row += 1
        ttk.Label(self.card, text="Itens:", font=("Arial", 13, "bold"), bootstyle="secondary").grid(row=row, column=0, sticky="w", padx=12, pady=(4,0))
        row += 1
        # Treeview para itens do recibo
        tree = ttk.Treeview(self.card, columns=("Nome", "Quantidade", "Preço"), show="headings", height=6)
        tree.heading("Nome", text="Nome")
        tree.heading("Quantidade", text="Qtd")
        tree.heading("Preço", text="Preço (R$)")
        tree.column("Nome", width=200, anchor="w")
        tree.column("Quantidade", width=60, anchor="center")
        tree.column("Preço", width=100, anchor="e")
        for p in produtos:
            tree.insert("", "end", values=(p['nome'], p['quantidade'], f"{p['preco']:.2f}"))
        tree.grid(row=row, column=0, padx=12, pady=2, sticky="ew")
        self.card.grid_rowconfigure(row, weight=1)
        row += 1
        ttk.Separator(self.card, orient="horizontal").grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        row += 1
        ttk.Label(self.card, text=f"Total: R$ {valor_total:.2f}", font=("Arial", 18, "bold"), bootstyle="success").grid(row=row, column=0, sticky="e", padx=12, pady=(8, 2))
        row += 1
        self.fechar_button = ttk.Button(self.card, text="Fechar Recibo", bootstyle="danger", command=self.esconder_recibo, width=22)
        self.fechar_button.grid(row=row, column=0, pady=(12, 4), sticky="ew")
        row += 1
        self.imprimir_button = ttk.Button(self.card, text="Imprimir Recibo", bootstyle="info", command=self.imprimir_recibo, width=22)
        self.imprimir_button.grid(row=row, column=0, pady=(0, 12), sticky="ew")
        self._recibo_para_imprimir = recibo_dados

    def esconder_recibo(self):
        for widget in self.card.winfo_children():
            widget.destroy()
        self._recibo_para_imprimir = None

    def imprimir_recibo(self):
        if not hasattr(self, '_recibo_para_imprimir') or not self._recibo_para_imprimir:
            messagebox.showerror("Erro", "Nenhum recibo para imprimir.")
            return
        recibo = self._recibo_para_imprimir
        texto = (
            f"GRAAL\n"
            f"Data: {recibo['data']}\n"
            f"Pedido: {recibo['pedido']}\n"
            f"CPF Cliente: {recibo['cpf_cliente']}\n"
            f"Produtos:\n{recibo['produtos_texto']}\n"
            f"Total: {recibo['total']}\n"
            f"Pagamento: {recibo['pagamento']}\n"
        )
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivo de Texto", "*.txt")],
                title="Salvar Recibo"
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(texto)
                messagebox.showinfo("Sucesso", f"Recibo salvo em: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar recibo", str(e))

    def on_show(self):
        self.carregar_comandas_fechadas()
        self.esconder_recibo()
        if hasattr(self.master, 'atualizar_comandas_e_recibo'):
            self.master.atualizar_comandas_e_recibo()
