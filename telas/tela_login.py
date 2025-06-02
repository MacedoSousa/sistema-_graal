import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from servicos.servico_funcionarios import autenticar, inicializar_cargos, cadastrar_funcionario
import sqlite3

def existe_usuario():
    try:
        conn = sqlite3.connect('graal.db')
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM funcionario')
        count = cur.fetchone()[0]
        conn.close()
        return count > 0
    except Exception:
        return False

def iniciar_tela_login():
    user_result = {'user': None}
    root = tk.Tk()
    root.withdraw()

    def mostrar_tela_cadastro():
        cadastro_win = tk.Toplevel(root)
        cadastro_win.title('Cadastro de Administrador')
        cadastro_win.geometry('420x420')
        cadastro_win.resizable(False, False)
        cadastro_win.configure(bg="#fffbe6")
        cadastro_win.grab_set()
        cadastro_win.focus_force()

        frame = ttk.Frame(cadastro_win, padding=35, bootstyle="light")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.config(borderwidth=2, relief="ridge")

        ttk.Label(frame, text="Cadastro do Primeiro Usuário", font=("Arial", 18, "bold"), bootstyle="primary").grid(row=0, column=0, columnspan=2, pady=(0, 25))
        ttk.Label(frame, text='Nome:', font=("Arial", 13), bootstyle="primary").grid(row=1, column=0, sticky="e", pady=10, padx=8)
        entry_nome = ttk.Entry(frame, font=("Arial", 13), width=22)
        entry_nome.grid(row=1, column=1, pady=10, padx=8)
        ttk.Label(frame, text='Usuário:', font=("Arial", 13), bootstyle="primary").grid(row=2, column=0, sticky="e", pady=10, padx=8)
        entry_usuario = ttk.Entry(frame, font=("Arial", 13), width=22)
        entry_usuario.grid(row=2, column=1, pady=10, padx=8)
        ttk.Label(frame, text='Senha:', font=("Arial", 13), bootstyle="primary").grid(row=3, column=0, sticky="e", pady=10, padx=8)
        entry_senha = ttk.Entry(frame, show='*', font=("Arial", 13), width=22)
        entry_senha.grid(row=3, column=1, pady=10, padx=8)
        ttk.Label(frame, text='Cargo:', font=("Arial", 13), bootstyle="primary").grid(row=4, column=0, sticky="e", pady=10, padx=8)
        entry_cargo = ttk.Label(frame, text='Gerente', font=("Arial", 13), bootstyle="info")
        entry_cargo.grid(row=4, column=1, pady=10, padx=8)
        def cadastrar():
            nome = entry_nome.get().strip()
            usuario = entry_usuario.get().strip()
            senha = entry_senha.get().strip()
            if not nome or not usuario or not senha:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            try:
                cadastrar_funcionario(nome, usuario, senha, "Gerente")
                messagebox.showinfo("Sucesso", "Administrador cadastrado com sucesso!")
                cadastro_win.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        ttk.Button(frame, text='Cadastrar', bootstyle="success", command=cadastrar, width=20).grid(row=5, column=0, columnspan=2, pady=28)
        entry_nome.focus()
        root.wait_window(cadastro_win)

    inicializar_cargos()
    if not existe_usuario():
        mostrar_tela_cadastro()

    login_win = tk.Toplevel(root)
    login_win.title('Login - Sistema GRAAL')
    login_win.geometry('420x380')
    login_win.resizable(False, False)
    login_win.configure(bg="#fffbe6")
    login_win.grab_set()
    login_win.focus_force()

    def tentar_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        user = autenticar(usuario, senha)
        if user:
            user_result['user'] = user
            login_win.destroy()
        else:
            messagebox.showerror('Erro', 'Usuário ou senha inválidos')

    frame = ttk.Frame(login_win, padding=35, bootstyle="light")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.config(borderwidth=2, relief="ridge")

    ttk.Label(frame, text="GRAAL VENDAS", font=("Arial", 22, "bold"), bootstyle="primary").grid(row=0, column=0, columnspan=2, pady=(0, 25))
    ttk.Label(frame, text='Usuário:', font=("Arial", 13), bootstyle="primary").grid(row=1, column=0, sticky="e", pady=10, padx=8)
    entry_usuario = ttk.Entry(frame, font=("Arial", 13), width=22)
    entry_usuario.grid(row=1, column=1, pady=10, padx=8)
    ttk.Label(frame, text='Senha:', font=("Arial", 13), bootstyle="primary").grid(row=2, column=0, sticky="e", pady=10, padx=8)
    entry_senha = ttk.Entry(frame, show='*', font=("Arial", 13), width=22)
    entry_senha.grid(row=2, column=1, pady=10, padx=8)
    ttk.Button(frame, text='Entrar', bootstyle="warning", command=tentar_login, width=20).grid(row=3, column=0, columnspan=2, pady=28)
    entry_usuario.focus()
    root.wait_window(login_win)
    return user_result['user']

if __name__ == '__main__':
    inicializar_cargos()
    user = iniciar_tela_login()
    if user:
        messagebox.showinfo('Bem-vindo', f'Bem-vindo, {user["nome"]} ({user["cargo"]})')
