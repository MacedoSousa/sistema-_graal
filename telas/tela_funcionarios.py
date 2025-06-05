import tkinter as tk
from tkinter import ttk, messagebox
from telas.tela_base import TelaBase
from servicos.servico_funcionarios import cadastrar_funcionario, listar_funcionarios

class TelaFuncionarios(TelaBase):
    def __init__(self, container):
        super().__init__(container, title="Funcionários")
        self._criar_widgets()

    def _criar_widgets(self):
        self.form_frame = ttk.LabelFrame(self, text="Cadastro de Funcionário", bootstyle="primary", padding=20)
        self.form_frame.grid(row=1, column=0, padx=30, pady=20, sticky="ew")
        self.form_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(self.form_frame, text="Nome:", font=("Arial", 12), bootstyle="primary").grid(row=0, column=0, sticky="e", pady=8, padx=8)
        self.entry_nome = ttk.Entry(self.form_frame, font=("Arial", 12))
        self.entry_nome.grid(row=0, column=1, pady=8, padx=8, sticky="ew")

        ttk.Label(self.form_frame, text="Usuário:", font=("Arial", 12), bootstyle="primary").grid(row=1, column=0, sticky="e", pady=8, padx=8)
        self.entry_usuario = ttk.Entry(self.form_frame, font=("Arial", 12))
        self.entry_usuario.grid(row=1, column=1, pady=8, padx=8, sticky="ew")

        ttk.Label(self.form_frame, text="Senha:", font=("Arial", 12), bootstyle="primary").grid(row=2, column=0, sticky="e", pady=8, padx=8)
        self.entry_senha = ttk.Entry(self.form_frame, show='*', font=("Arial", 12))
        self.entry_senha.grid(row=2, column=1, pady=8, padx=8, sticky="ew")

        ttk.Label(self.form_frame, text="Cargo:", font=("Arial", 12), bootstyle="primary").grid(row=3, column=0, sticky="e", pady=8, padx=8)
        self.combo_cargo = ttk.Combobox(self.form_frame, values=["Gerente", "Vendedor", "Repositor"], font=("Arial", 12), state="readonly")
        self.combo_cargo.grid(row=3, column=1, pady=8, padx=8, sticky="ew")
        self.combo_cargo.current(0)

        self.btn_cadastrar = ttk.Button(self.form_frame, text="Cadastrar Funcionário", bootstyle="success", command=self.cadastrar_funcionario, width=22)
        self.btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=18)

        self.listagem_frame = ttk.LabelFrame(self, text="Funcionários Cadastrados", bootstyle="info", padding=12)
        self.listagem_frame.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
        self.treeview = ttk.Treeview(self.listagem_frame, columns=("ID", "Nome", "Usuário", "Cargo"), show="headings")
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Nome", text="Nome")
        self.treeview.heading("Usuário", text="Usuário")
        self.treeview.heading("Cargo", text="Cargo")
        self.treeview.column("ID", width=60)
        self.treeview.column("Nome", width=150)
        self.treeview.column("Usuário", width=120)
        self.treeview.column("Cargo", width=100)
        self.treeview.pack(fill="both", expand=True)
        self.atualizar_listagem_funcionarios()

    def atualizar_listagem_funcionarios(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for funcionario in listar_funcionarios():
            self.treeview.insert("", "end", values=(funcionario['id'], funcionario['nome'], funcionario['usuario'], funcionario['cargo']))

    def cadastrar_funcionario(self):
        nome = self.entry_nome.get().strip()
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        cargo = self.combo_cargo.get().strip()
        if not nome or not usuario or not senha or not cargo:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        try:
            cadastrar_funcionario(nome, usuario, senha, cargo)
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            self.entry_nome.delete(0, tk.END)
            self.entry_usuario.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            self.combo_cargo.current(0)
            self.atualizar_listagem_funcionarios()
            if hasattr(self.master, 'atualizar_funcionarios_e_inicial'):
                self.master.atualizar_funcionarios_e_inicial()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def excluir_funcionario(self):
        item_selecionado = self.treeview.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione um funcionário para excluir.")
            return
        funcionario_id = self.treeview.item(item_selecionado[0], 'values')[0]
        if messagebox.askyesno("Confirmação", f"Deseja excluir o funcionário de ID {funcionario_id}?"):
            try:
                from servicos.servico_funcionarios import excluir_funcionario
                excluir_funcionario(funcionario_id)
                self.atualizar_listagem_funcionarios()
                messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
                if hasattr(self.master, 'atualizar_funcionarios_e_inicial'):
                    self.master.atualizar_funcionarios_e_inicial()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir funcionário: {e}")

    def on_show(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.combo_cargo.current(0)
        self.atualizar_listagem_funcionarios()
        if hasattr(self.master, 'atualizar_funcionarios_e_inicial'):
            self.master.atualizar_funcionarios_e_inicial()
