import tkinter as tk
from tkinter import ttk, messagebox
from telas.constantes import get_cor
from servicos.servico_produtos import listar_produtos, salvar_produto, excluir_produto

class TelaProdutos(tk.Frame):
    def __init__(self, master, atualizar_todas_listas=None):
        super().__init__(master)
        self.atualizar_todas_listas = atualizar_todas_listas
        self.produtos_feedback_var = tk.StringVar()
        self.produtos_feedback_label = tk.Label(self, textvariable=self.produtos_feedback_var, font=("Segoe UI", 11, "bold"), bg='#f6faff', fg='#e53e3e')
        self.produtos_feedback_label.pack(fill='x', padx=32, pady=(8, 0))
        self.produtos_feedback_label.pack_forget()
        self.criar_card_produtos()

    def criar_card_produtos(self):
        # Cabeçalho
        cabecalho_frame = tk.Frame(self, bg=get_cor("cabecalho"))
        cabecalho_frame.pack(fill='x')

        titulo = tk.Label(cabecalho_frame, text="Produtos", bg=get_cor("cabecalho"), fg="white", font=("Segoe UI", 16, "bold"))
        titulo.pack(side='left', padx=10, pady=10)

        # Botão Adicionar Produto
        botao_adicionar = tk.Button(
            cabecalho_frame,
            text="Adicionar Produto",
            command=self.abrir_modal_produto_moderno,
            bg="#22c55e",
            activebackground="#16a34a",
            fg="white",
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        botao_adicionar.pack(side='right', padx=10, pady=10)

        # Tabela de Produtos (agora com coluna Peso/Unidade)
        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Preço", "Quantidade", "Peso/Unidade"), show="headings")
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        for coluna in self.tree["columns"]:
            self.tree.heading(coluna, text=coluna)

        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Segoe UI", 12), rowheight=30)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 14, "bold"))

        barra_rolagem = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        barra_rolagem.pack(side='right', fill='y')
        self.tree.configure(yscroll=barra_rolagem.set)

        self.atualizar_lista_produtos()

        # Evento duplo clique para editar produto
        self.tree.bind("<Double-1>", self.editar_produto_por_duplo_clique)
        # Remove binding de clique simples para editar
        self.tree.unbind("<Button-1>")

    def atualizar_lista_produtos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        produtos = listar_produtos()
        for produto in produtos:
            # Exibe unidade junto ao peso, se disponível
            unidade = produto.get('unidade', '')
            peso = produto.get('peso', '')
            if unidade and peso:
                peso_fmt = f"{peso} {unidade}"
            else:
                peso_fmt = peso or ''
            self.tree.insert("", "end", values=(
                produto.get('id', ''),
                produto.get('nome', ''),
                produto.get('preco', ''),
                produto.get('quantidade', ''),
                peso_fmt
            ))

    def abrir_modal_produto_moderno(self, produto=None):
        # Criação da janela modal
        self.modal = tk.Toplevel(self)
        self.modal.title("Adicionar/Editar Produto")
        self.modal.geometry("420x600")  # Aumenta altura para garantir espaço para botões
        self.modal.resizable(False, False)
        self.modal.grab_set()  # Foca a janela modal

        # Campos do formulário
        labels = [
            ("Nome:", "entry_nome"),
            ("Código de Barras:", "entry_codigo_barras"),
            ("Preço (R$):", "entry_preco"),
            ("Data de Validade (AAAA-MM-DD):", "entry_validade"),
            ("Peso:", "entry_peso"),
            ("Unidade:", "entry_unidade"),
            ("Fornecedor:", "entry_fornecedor"),
            ("Estoque:", "entry_estoque")
        ]
        self.entries = {}
        for label_text, entry_attr in labels:
            tk.Label(self.modal, text=label_text, anchor='w').pack(fill='x', padx=24, pady=(12, 0))
            if entry_attr == "entry_unidade":
                self.entry_unidade = ttk.Combobox(self.modal, font=("Segoe UI", 12), state="readonly")
                self.entry_unidade['values'] = ("kg", "g", "L", "ml")
                self.entry_unidade.current(0)
                self.entry_unidade.pack(fill='x', padx=24, pady=(0, 8))
                self.entries[entry_attr] = self.entry_unidade
            else:
                entry = tk.Entry(self.modal, font=("Segoe UI", 12))
                entry.pack(fill='x', padx=24, pady=(0, 8))
                self.entries[entry_attr] = entry
                setattr(self, entry_attr, entry)

        # Espaço expansível para empurrar os botões para o rodapé
        tk.Frame(self.modal, bg='#f6faff').pack(fill='both', expand=True)

        # Botões
        frame_botoes = tk.Frame(self.modal, bg='#f6faff')
        frame_botoes.pack(side='bottom', pady=16, padx=16, fill='x')

        botao_salvar = tk.Button(
            frame_botoes,
            text="Salvar",
            command=lambda: self.salvar_produto(produto),
            bg="#2563eb",
            activebackground="#1d4ed8",
            fg="white",
            activeforeground="white",
            font=("Segoe UI", 13, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            width=12,
            bd=0
        )
        botao_salvar.pack(side='left', padx=6, pady=0, fill='x', expand=True)

        if produto:
            def excluir_e_fechar():
                self.excluir_produto_moderno(produto)
                self.modal.destroy()
            botao_excluir = tk.Button(
                frame_botoes,
                text="Excluir",
                command=excluir_e_fechar,
                bg="#e53e3e",
                activebackground="#b91c1c",
                fg="white",
                activeforeground="white",
                font=("Segoe UI", 13, "bold"),
                relief=tk.FLAT,
                cursor="hand2",
                height=2,
                width=12,
                bd=0
            )
            botao_excluir.pack(side='left', padx=6, pady=0, fill='x', expand=True)

        botao_cancelar = tk.Button(
            frame_botoes,
            text="Cancelar",
            command=self.modal.destroy,
            bg="#6b7280",
            activebackground="#374151",
            fg="white",
            activeforeground="white",
            font=("Segoe UI", 13, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            width=12,
            bd=0
        )
        botao_cancelar.pack(side='left', padx=6, pady=0, fill='x', expand=True)

        # Preenche os campos se for edição
        if produto:
            # Se for tupla/lista da treeview, busca o produto completo pelo ID
            if not isinstance(produto, dict):
                try:
                    from servicos.servico_produtos import obter_produto_por_codigo
                    produto_dict = obter_produto_por_codigo(produto[0])
                except Exception:
                    produto_dict = None
            else:
                produto_dict = produto
            if produto_dict:
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, produto_dict.get('nome', ''))
                self.entry_codigo_barras.delete(0, tk.END)
                self.entry_codigo_barras.insert(0, produto_dict.get('codigo_de_barras', ''))
                self.entry_preco.delete(0, tk.END)
                self.entry_preco.insert(0, produto_dict.get('preco', ''))
                self.entry_validade.delete(0, tk.END)
                self.entry_validade.insert(0, produto_dict.get('data_validade', ''))
                self.entry_peso.delete(0, tk.END)
                self.entry_peso.insert(0, produto_dict.get('peso_kg', ''))
                unidade = produto_dict.get('unidade', 'kg')
                if unidade in ("kg", "g", "L", "ml"):
                    self.entry_unidade.set(unidade)
                else:
                    self.entry_unidade.set("kg")
                self.entry_fornecedor.delete(0, tk.END)
                self.entry_fornecedor.insert(0, produto_dict.get('fornecedor', ''))
                self.entry_estoque.delete(0, tk.END)
                self.entry_estoque.insert(0, produto_dict.get('estoque', ''))

    def salvar_produto(self, produto_existente):
        # Coleta os dados dos campos
        nome = self.entry_nome.get().strip()
        codigo_barras = self.entry_codigo_barras.get().strip()
        preco = self.entry_preco.get().strip()
        validade = self.entry_validade.get().strip()
        peso = self.entry_peso.get().strip()
        unidade = self.entry_unidade.get().strip()
        fornecedor = self.entry_fornecedor.get().strip()
        estoque = self.entry_estoque.get().strip()

        # Validação básica
        if not all([nome, codigo_barras, preco, validade, peso, fornecedor, estoque]):
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
            return
        try:
            preco = float(preco)
            peso = float(peso)
            estoque = int(estoque)
            codigo_barras = int(codigo_barras)
        except ValueError:
            messagebox.showwarning("Atenção", "Preço, Peso, Estoque e Código de Barras devem ser numéricos.")
            return

        produto_dict = {
            'nome': nome,
            'codigo_de_barras': codigo_barras,
            'preco': preco,
            'data_validade': validade,
            'peso_kg': peso,
            'unidade': unidade,
            'fornecedor': fornecedor,
            'estoque': estoque
        }
        if produto_existente:
            # Edição: precisa do id
            produto_dict['id_produto'] = produto_existente[0] if not isinstance(produto_existente, dict) else produto_existente.get('id')
            # Chama função de atualização
            from servicos.database import conectar_banco_de_dados
            from servicos.servico_produtos import atualizar_produto
            conn = conectar_banco_de_dados()
            if conn:
                atualizar_produto(conn, produto_dict)
                conn.close()
        else:
            # Novo produto
            from servicos.servico_produtos import salvar_novo_produto
            salvar_novo_produto(produto_dict)

        self.modal.destroy()
        self.atualizar_lista_produtos()
        if self.atualizar_todas_listas:
            self.atualizar_todas_listas()

    def editar_produto_por_duplo_clique(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            produto = self.tree.item(item_selecionado)["values"]
            self.abrir_modal_produto_moderno(produto)

    def excluir_produto_moderno(self, produto):
        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o produto {produto[1]}?")
        if resposta:
            excluir_produto(produto[0])
            self.atualizar_lista_produtos()
            self.atualizar_todas_listas()

    def excluir_produto_selecionado(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para excluir.")
            return
        produto = self.tree.item(item_selecionado)["values"]
        if not produto:
            return
        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o produto {produto[1]}?")
        if resposta:
            excluir_produto(produto[0])
            self.atualizar_lista_produtos()
            if self.atualizar_todas_listas:
                self.atualizar_todas_listas()

    # Outros métodos auxiliares se necessário
