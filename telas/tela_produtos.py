import tkinter as tk
from tkinter import ttk, messagebox
from telas.tela_base import TelaBase
from servicos.servico_produtos import (
    salvar_novo_produto,
    obter_todos_os_produtos_dict,
    atualizar_produto,
    excluir_produto,
    obter_proximo_codigo
)

class TelaProdutos(TelaBase):
    def __init__(self, container, conn=None):
        super().__init__(container, title="Produtos")
        self.item_selecionado = None
        self.produtos = []
        self.codigo_produto_atual = obter_proximo_codigo(None)

        self.form_frame = ttk.LabelFrame(self, text="Dados do Produto", bootstyle="primary")

        self.nome_label = ttk.Label(self.form_frame, text="Nome:", bootstyle="primary")
        self.nome_entry = ttk.Entry(self.form_frame)

        self.empresa_label = ttk.Label(self.form_frame, text="Empresa:", bootstyle="primary")
        self.empresa_entry = ttk.Entry(self.form_frame)

        self.peso_label = ttk.Label(self.form_frame, text="Peso:", bootstyle="primary")
        self.peso_entry = ttk.Entry(self.form_frame)
        self.peso_unidades = ttk.Combobox(self.form_frame, values=["Kg", "g", "L", 'ml'], width=5)
        self.peso_unidades.set("Kg")

        self.preco_label = ttk.Label(self.form_frame, text="Preço (R$):", bootstyle="primary")
        self.preco_entry = ttk.Entry(self.form_frame)

        self.validade_label = ttk.Label(self.form_frame, text="Validade (AAAA-MM-DD):", bootstyle="primary")
        self.validade_entry = ttk.Entry(self.form_frame)

        self.quantidade_label = ttk.Label(self.form_frame, text="Quantidade:", bootstyle="primary")
        self.quantidade_entry = ttk.Entry(self.form_frame)

        self.salvar_button = ttk.Button(self.form_frame, text="Salvar Produto", bootstyle="warning", command=self.salvar_produto)
        self.limpar_button = ttk.Button(self.form_frame, text="Limpar", bootstyle="secondary", command=self.limpar_formulario)

        
        self.nome_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.empresa_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.empresa_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.peso_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.peso_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.peso_unidades.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        self.preco_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.preco_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.validade_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.validade_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.quantidade_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.quantidade_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        self.salvar_button.grid(row=6, column=0, padx=5, pady=10, sticky="ew")
        self.limpar_button.grid(row=6, column=1, padx=5, pady=10, sticky="ew")

        self.form_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


        self.listagem_frame = ttk.LabelFrame(self, text="Produtos Cadastrados", bootstyle="primary")
        self.treeview = ttk.Treeview(self.listagem_frame,
                                        columns=("Codigo", "Nome", "Empresa", "Peso", "Preco", "Validade", "Quantidade"),
                                        show="headings")

        
        self.treeview.heading("Codigo", text="Codigo")
        self.treeview.heading("Nome", text="Nome")
        self.treeview.heading("Empresa", text="Empresa")
        self.treeview.heading("Peso", text="Peso")
        self.treeview.heading("Preco", text="Preço (R$)")
        self.treeview.heading("Validade", text="Validade")
        self.treeview.heading("Quantidade", text="Quantidade")

        
        self.treeview.column("Codigo", width=80)
        self.treeview.column("Nome", width=150)
        self.treeview.column("Empresa", width=100)
        self.treeview.column("Peso", width=80)
        self.treeview.column("Preco", width=80)
        self.treeview.column("Validade", width=100)
        self.treeview.column("Quantidade", width=80)
        self.acoes_frame = ttk.Frame(self)

        self.treeview.bind("<Double-1>", self.selecionar_produto_para_editar)
        self.treeview.pack(fill="both", expand=True)
        self.listagem_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        self.acoes_frame.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        self.editar_button = ttk.Button(self.acoes_frame, text="Editar", bootstyle="info", command=self.editar_produto)
        self.excluir_button = ttk.Button(self.acoes_frame, text="Excluir", bootstyle="danger", command=self.excluir_produto)

        self.editar_button.grid(row=0, column=0, padx=5)
        self.excluir_button.grid(row=0, column=1, padx=5)
        self.acoes_frame.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        self.carregar_produtos()
        self._agendar_atualizacao()

    def _agendar_atualizacao(self):
        self.after(2000, self._atualizacao_periodica)

    def _atualizacao_periodica(self):
        self.carregar_produtos()
        self._agendar_atualizacao()

    def carregar_produtos(self):
        self.produtos = obter_todos_os_produtos_dict()
        self.atualizar_listagem()

    def atualizar_listagem(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for produto in self.produtos:
            self.treeview.insert("", "end", values=(
                produto.get("codigo_de_barras", produto.get("id_produto", "")),
                produto["nome"],
                produto.get("fornecedor", ""),
                f"{produto.get('peso_kg', '')}",
                produto["preco"],
                produto.get("data_validade", ""),
                produto["estoque"]
            ))

    def selecionar_produto_para_editar(self, event):
        selecionados = self.treeview.selection()
        if selecionados:
            item_id = selecionados[0]
            produto_selecionado = self.treeview.item(item_id, 'values')
            if produto_selecionado:
                codigo, nome, empresa, peso_unidade, preco, validade, quantidade = produto_selecionado
                try:
                    peso, unidade = peso_unidade.split()
                    self.nome_entry.delete(0, tk.END)
                    self.nome_entry.insert(0, nome)
                    self.empresa_entry.delete(0, tk.END)
                    self.empresa_entry.insert(0, empresa)
                    self.peso_entry.delete(0, tk.END)
                    self.peso_entry.insert(0, peso)
                    self.peso_unidades.set(unidade)
                    self.preco_entry.delete(0, tk.END)
                    self.preco_entry.insert(0, preco)
                    self.validade_entry.delete(0, tk.END)
                    self.validade_entry.insert(0, validade)
                    self.quantidade_entry.delete(0, tk.END)
                    self.quantidade_entry.insert(0, quantidade)
                    self.item_selecionado = item_id
                except ValueError as e:
                    messagebox.showerror("Erro ao Editar",
                                         f"Formato de peso inválido para o produto: '{peso_unidade}'. Erro: {e}")
        else:
            messagebox.showerror("Erro", "Selecione um produto para editar.")

    def salvar_produto(self):
        nome = self.nome_entry.get().strip()
        empresa = self.empresa_entry.get().strip()
        peso = self.peso_entry.get().strip()
        unidade_peso = self.peso_unidades.get()
        preco_str = self.preco_entry.get().strip()
        validade = self.validade_entry.get().strip()
        quantidade_str = self.quantidade_entry.get().strip()

        if not nome:
            messagebox.showerror("Erro", "O nome do produto é obrigatório.")
            return
        if not preco_str:
            messagebox.showerror("Erro", "O preço do produto é obrigatório.")
            return
        try:
            preco = float(preco_str)
            if preco < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "O preço deve ser um número válido e não negativo.")
            return
        if not quantidade_str:
            messagebox.showerror("Erro", "A quantidade do produto é obrigatória.")
            return
        try:
            quantidade = int(quantidade_str)
            if quantidade < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro válido e não negativo.")
            return

        for produto in self.produtos:
            if produto["nome"].lower() == nome.lower() and (not self.item_selecionado or produto["id_produto"] != self.treeview.item(self.item_selecionado, 'values')[0]):
                messagebox.showerror("Erro", "Já existe um produto com este nome.")
                return
        produto_atualizado = {
            "id_produto": self.treeview.item(self.item_selecionado, 'values')[0] if self.item_selecionado else obter_proximo_codigo(None),
            "codigo_de_barras": self.codigo_produto_atual,
            "nome": nome,
            "fornecedor": empresa,
            "peso_kg": f"{peso} {unidade_peso}",
            "preco": float(preco_str),
            "data_validade": validade,
            "estoque": int(quantidade_str)
        }
        try:
            if self.item_selecionado:
                atualizar_produto(None, produto_atualizado)
                for i, produto in enumerate(self.produtos):
                    if str(produto.get("id_produto", produto.get("codigo_de_barras"))) == str(produto_atualizado["id_produto"]):
                        self.produtos[i] = produto_atualizado
                        break
                self.atualizar_listagem()
                self.item_selecionado = None
                self.salvar_button.config(text="Salvar Produto")
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            else:
                salvar_novo_produto(produto_atualizado)
                self.produtos.append(produto_atualizado)
                self.atualizar_listagem()
                self.codigo_produto_atual = obter_proximo_codigo(None)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_formulario()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {e}")

    def editar_produto(self):
        if not self.treeview.selection():
            messagebox.showerror("Erro", "Selecione um produto para editar.")
            return
        self.salvar_button.config(text="Atualizar Produto")
        self.selecionar_produto_para_editar("<Double-1>")

    def excluir_produto(self):
        item_selecionado = self.treeview.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione um produto para excluir.")
            return
        codigo_excluir = self.treeview.item(item_selecionado[0], 'values')[0]
        if messagebox.askyesno("Confirmação", f"Deseja excluir o produto com código {codigo_excluir}?"):
            try:
                excluir_produto(codigo_excluir)
                self.produtos = [p for p in self.produtos if str(p.get("codigo_de_barras", p.get("id_produto"))) != str(codigo_excluir)]
                self.atualizar_listagem()
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir produto: {e}")

    def limpar_formulario(self):
        self.nome_entry.delete(0, tk.END)
        self.empresa_entry.delete(0, tk.END)
        self.peso_entry.delete(0, tk.END)
        self.peso_unidades.set("Kg")
        self.preco_entry.delete(0, tk.END)
        self.validade_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.item_selecionado = None
        self.salvar_button.config(text="Salvar Produto")