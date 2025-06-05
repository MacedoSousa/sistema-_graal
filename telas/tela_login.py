import tkinter as tk
from tkinter import messagebox
from telas.constantes import get_cor, centralizar_janela
from servicos.servico_funcionarios import autenticar
from PIL import Image, ImageTk
import os

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color='#bdbdbd', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()
    def put_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color
    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

def iniciar_tela_login():
    login_win = tk.Tk()
    login_win.title("Sistema de Vendas | Login")
    login_win.geometry("500x520")
    login_win.configure(bg='#f6faff')
    login_win.resizable(False, False)

    sombra = tk.Frame(login_win, bg='#e3e8ee', highlightthickness=0, bd=0)
    sombra.place(relx=0.5, rely=0.5, anchor="center", width=420, height=440, x=10, y=10)
    card = tk.Frame(login_win, bg='white', highlightthickness=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=410, height=430)
    card.config(bd=0)
    card.configure(highlightbackground='#e3e8ee', highlightcolor='#e3e8ee', highlightthickness=2)
    card.pack_propagate(False)

    img_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'graal.jpg')
    try:
        img = Image.open(img_path)
        img = img.resize((90, 90))
        foto = ImageTk.PhotoImage(img)
        img_label = tk.Label(card, image=foto, bg='white')
        img_label.image = foto
        img_label.pack(pady=(18, 0))
    except Exception as e:
        pass

    tk.Label(card, text="Bem-vindo!", font=("Segoe UI", 20, "bold"), bg='white', fg='#23272b').pack(pady=(18, 0))
    tk.Label(card, text="Acesse sua conta para continuar", font=("Segoe UI", 12), bg='white', fg='#7b7b7b').pack(pady=(2, 18))

    usuario_label = tk.Label(card, text="Usuário", font=("Segoe UI", 11, "bold"), bg='white', fg='#23272b')
    usuario_label.pack(anchor='w', padx=38, pady=(0, 0))
    entry_usuario = PlaceholderEntry(card, placeholder="Digite seu usuário", font=("Segoe UI", 12), fg='#23272b', bg='#f6faff', relief="flat", bd=0, highlightthickness=0)
    entry_usuario.pack(fill='x', padx=38, pady=(0, 14), ipady=9)

    senha_label = tk.Label(card, text="Senha", font=("Segoe UI", 11, "bold"), bg='white', fg='#23272b')
    senha_label.pack(anchor='w', padx=38, pady=(0, 0))
    senha_frame = tk.Frame(card, bg='white')
    senha_frame.pack(fill='x', padx=38, pady=(0, 20))
    entry_senha = PlaceholderEntry(senha_frame, placeholder="Digite sua senha", font=("Segoe UI", 12), fg='#23272b', bg='#f6faff', relief="flat", bd=0, highlightthickness=0, show='*')
    entry_senha.pack(side='left', fill='x', expand=True, ipady=9)
    def toggle_senha():
        if entry_senha.cget('show') == '':
            entry_senha.config(show='*')
        else:
            entry_senha.config(show='')
    btn_olho = tk.Button(senha_frame, text='👁️', font=("Segoe UI", 12), fg='#23272b', bg='#f6faff', relief='flat', bd=0, command=toggle_senha, activebackground='#e3e8ee')
    btn_olho.pack(side='right', padx=(6, 0))

    user_result = {'user': None}

    def login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        if usuario == entry_usuario.placeholder:
            usuario = ''
        if senha == entry_senha.placeholder:
            senha = ''
        entry_usuario.config(highlightbackground='#e3e8ee')
        entry_senha.config(highlightbackground='#e3e8ee')
        if not usuario or not senha:
            entry_usuario.config(highlightbackground='#ff4d4f')
            entry_senha.config(highlightbackground='#ff4d4f')
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        user = autenticar(usuario, senha)
        if user:
            user_result['user'] = user
            login_win.destroy()
        else:
            entry_usuario.config(highlightbackground='#ff4d4f')
            entry_senha.config(highlightbackground='#ff4d4f')
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def on_enter(event=None):
        login()

    def on_enter_btn(e):
        btn_login.config(bg='#2563eb', fg='white')
    def on_leave_btn(e):
        btn_login.config(bg='#23272b', fg='white')
    btn_login = tk.Button(card, text="Entrar", font=("Segoe UI", 13, "bold"), bg='#23272b', fg='white', relief="flat", bd=0, command=on_enter, activebackground='#2563eb', activeforeground='white', cursor='hand2')
    btn_login.pack(pady=(8, 0), ipadx=8, ipady=10, fill='x', padx=38)
    btn_login.bind("<Enter>", on_enter_btn)
    btn_login.bind("<Leave>", on_leave_btn)

    login_win.bind('<Return>', on_enter)
    entry_usuario.focus()
    login_win.update_idletasks()
    centralizar_janela(login_win, 500, 520)
    login_win.mainloop()
    return user_result['user']
