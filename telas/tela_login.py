import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
import os
from servicos.servico_funcionarios import autenticar, inicializar_cargos, cadastrar_funcionario
from servicos.utils import campo_obrigatorio, logar_erro

DB_PATH = 'graal.db'

def existe_usuario():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM funcionario')
            count = cur.fetchone()[0]
            return count > 0
    except sqlite3.Error:
        return False

def mostrar_tela_cadastro(root):
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

    ttk.Label(frame, text="Cadastro do Primeiro Usuário", font=("Arial", 18, "bold"), bootstyle="primary")\
        .grid(row=0, column=0, columnspan=2, pady=(0, 25))

    labels = ["Nome", "Usuário", "Senha", "Cargo"]
    for i, text in enumerate(labels[:-1], start=1):
        ttk.Label(frame, text=f'{text}:', font=("Arial", 13), bootstyle="primary")\
            .grid(row=i, column=0, sticky="e", pady=10, padx=8)

    entry_nome = ttk.Entry(frame, font=("Arial", 13), width=22)
    entry_usuario = ttk.Entry(frame, font=("Arial", 13), width=22)
    entry_senha = ttk.Entry(frame, show='*', font=("Arial", 13), width=22)

    entry_nome.grid(row=1, column=1, pady=10, padx=8)
    entry_usuario.grid(row=2, column=1, pady=10, padx=8)
    entry_senha.grid(row=3, column=1, pady=10, padx=8)

    ttk.Label(frame, text='Cargo:', font=("Arial", 13), bootstyle="primary")\
        .grid(row=4, column=0, sticky="e", pady=10, padx=8)
    ttk.Label(frame, text='Gerente', font=("Arial", 13), bootstyle="info")\
        .grid(row=4, column=1, pady=10, padx=8)

    def cadastrar():
        nome = entry_nome.get().strip()
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()

        if not campo_obrigatorio(nome) or not campo_obrigatorio(usuario) or not campo_obrigatorio(senha):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            cadastrar_funcionario(nome, usuario, senha, "Gerente")
            messagebox.showinfo("Sucesso", "Administrador cadastrado com sucesso!")
            cadastro_win.destroy()
        except Exception as e:
            logar_erro(e)
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    ttk.Button(frame, text='Cadastrar', bootstyle="success", command=cadastrar, width=20)\
        .grid(row=5, column=0, columnspan=2, pady=28)

    entry_nome.focus()
    root.wait_window(cadastro_win)

def iniciar_tela_login():
    user_result = {'user': None}
    root = tk.Tk()
    root.withdraw()
    inicializar_cargos()
    if not existe_usuario():
        mostrar_tela_cadastro(root)
    login_win = tk.Toplevel(root)
    login_win.title('Login - Sistema GRAAL')
    login_win.geometry('900x600+100+50')
    login_win.resizable(False, False)
    login_win.configure(bg="#181c1f")
    img_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'graal.jpg')
    img = Image.open(img_path)
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.LANCZOS
    img = img.resize((120, 120), resample)
    logo_img = ImageTk.PhotoImage(img)
    logo_label = tk.Label(login_win, image=logo_img, bg="#181c1f")
    logo_label.image = logo_img
    logo_label.place(relx=0.5, rely=0.22, anchor="center")

    frame = ttk.Frame(login_win, padding=40, bootstyle="dark")
    frame.place(relx=0.5, rely=0.65, anchor="center")

    ttk.Label(frame, text="Usuário:", font=("Arial", 14), bootstyle="primary")\
        .grid(row=0, column=0, pady=10, padx=8, sticky="e")
    ttk.Label(frame, text="Senha:", font=("Arial", 14), bootstyle="primary")\
        .grid(row=1, column=0, pady=10, padx=8, sticky="e")

    entry_usuario = ttk.Entry(frame, font=("Arial", 14), width=22)
    entry_senha = ttk.Entry(frame, show='*', font=("Arial", 14), width=22)
    entry_usuario.grid(row=0, column=1, pady=10, padx=8)
    entry_senha.grid(row=1, column=1, pady=10, padx=8)

    def login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()

        if not campo_obrigatorio(usuario) or not campo_obrigatorio(senha):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        user = autenticar(usuario, senha)
        if user:
            user_result['user'] = user
            login_win.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    ttk.Button(frame, text='Entrar', bootstyle="success", command=login, width=20)\
        .grid(row=2, column=0, columnspan=2, pady=28)

    entry_usuario.focus()
    root.wait_window(login_win)
    return user_result['user']

if __name__ == '__main__':
    user = iniciar_tela_login()
    if user:
        messagebox.showinfo('Bem-vindo', f'Bem-vindo, {user["nome"]} ({user["cargo"]})')
