import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from servicos.servico_funcionarios import cadastrar_funcionario

class TelaCadastroFuncionario(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=30, pady=30, fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        frame = ttk.LabelFrame(self, text="Cadastro de Funcionário", bootstyle="primary", padding=20)
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Nome:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=8, padx=8)
        self.entry_nome = ttk.Entry(frame, font=("Arial", 12), width=25)
        self.entry_nome.grid(row=0, column=1, pady=8, padx=8)

        ttk.Label(frame, text="Usuário:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=8, padx=8)
        self.entry_usuario = ttk.Entry(frame, font=("Arial", 12), width=25)
        self.entry_usuario.grid(row=1, column=1, pady=8, padx=8)

        ttk.Label(frame, text="Senha:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=8, padx=8)
        self.entry_senha = ttk.Entry(frame, show='*', font=("Arial", 12), width=25)
        self.entry_senha.grid(row=2, column=1, pady=8, padx=8)

        ttk.Label(frame, text="Cargo:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=8, padx=8)
        self.combo_cargo = ttk.Combobox(frame, values=["Gerente", "Vendedor", "Repositor"], font=("Arial", 12), width=23)
        self.combo_cargo.grid(row=3, column=1, pady=8, padx=8)
        self.combo_cargo.current(0)

        btn_cadastrar = ttk.Button(frame, text="Cadastrar", bootstyle="success", command=self.cadastrar_funcionario, width=18)
        btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=18)

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
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    TelaCadastroFuncionario(root)
    root.mainloop()
