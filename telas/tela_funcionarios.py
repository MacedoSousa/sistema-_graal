import tkinter as tk
from PIL import Image, ImageTk
from telas.constantes import get_cor
from servicos.servico_funcionarios import listar_funcionarios
import os
from tkinter import ttk

class TelaFuncionarios(tk.Frame):
    def __init__(self, master, atualizar_todas_listas=None):
        super().__init__(master, bg='#f6faff')
        self.atualizar_todas_listas = atualizar_todas_listas
        self.fotos = {}
        self.criar_cards_funcionarios()

    def criar_cards_funcionarios(self):
        for widget in self.winfo_children():
            widget.destroy()
        cabecalho = tk.Frame(self, bg=get_cor("cabecalho"))
        cabecalho.pack(fill='x')
        tk.Label(cabecalho, text="Funcionários", bg=get_cor("cabecalho"), fg="white", font=("Segoe UI", 16, "bold")).pack(side='left', padx=10, pady=10)
        btn_add = tk.Button(cabecalho, text="Adicionar Funcionário", command=self.abrir_modal_adicionar, bg="#2563eb", fg="white", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, cursor="hand2")
        btn_add.pack(side='right', padx=10, pady=10)
        self.cards_frame = tk.Frame(self, bg='#f6faff')
        self.cards_frame.pack(fill='both', expand=True, padx=20, pady=10)
        funcionarios = listar_funcionarios()
        if not funcionarios:
            tk.Label(self.cards_frame, text="Nenhum funcionário cadastrado.", font=("Segoe UI", 12), bg='#f6faff', fg='#e53e3e').pack(pady=18)
            return
        for f in funcionarios:
            card = tk.Frame(self.cards_frame, bg='white', highlightbackground='#e3e8ee', highlightthickness=2, bd=0)
            card.pack(fill='x', pady=8, padx=0)
            frame_img = tk.Frame(card, bg='white')
            frame_img.pack(side='left', padx=18, pady=10)
            img_path = f.get('foto') or os.path.join('img', 'graal.jpg')
            try:
                img = Image.open(img_path)
                img = img.resize((64, 64))
                foto = ImageTk.PhotoImage(img)
            except Exception:
                img = Image.new('RGB', (64, 64), color='#e3e8ee')
                foto = ImageTk.PhotoImage(img)
            self.fotos[f['id']] = foto
            tk.Label(frame_img, image=foto, bg='white').pack()
            info = tk.Frame(card, bg='white')
            info.pack(side='left', padx=18, pady=10, fill='x', expand=True)
            tk.Label(info, text=f.get('nome', ''), font=("Segoe UI", 15, "bold"), bg='white', fg='#23272b').pack(anchor='w')
            tk.Label(info, text=f.get('cargo', ''), font=("Segoe UI", 12), bg='white', fg='#2563eb').pack(anchor='w', pady=(2, 0))
            btn_edit = tk.Button(card, text="Editar", command=lambda fid=f['id']: self.abrir_modal_editar(fid), bg="#2563eb", fg="white", font=("Segoe UI", 11), relief=tk.FLAT, cursor="hand2")
            btn_edit.pack(side='right', padx=10, pady=10)
            btn_del = tk.Button(card, text="Excluir", command=lambda fid=f['id']: self.excluir_funcionario(fid), bg="#e53e3e", fg="white", font=("Segoe UI", 11), relief=tk.FLAT, cursor="hand2")
            btn_del.pack(side='right', padx=0, pady=10)

    def abrir_modal_adicionar(self):
        # Modal de cadastro de funcionário
        modal = tk.Toplevel(self)
        modal.title("Adicionar Funcionário")
        modal.geometry("400x350")
        modal.configure(bg='#f6faff')
        modal.transient(self)
        modal.grab_set()
        
        tk.Label(modal, text="Nome:", font=("Segoe UI", 12), bg='#f6faff').pack(anchor='w', padx=24, pady=(18, 0))
        entry_nome = tk.Entry(modal, font=("Segoe UI", 12))
        entry_nome.pack(fill='x', padx=24, pady=(0, 8))
        tk.Label(modal, text="Usuário:", font=("Segoe UI", 12), bg='#f6faff').pack(anchor='w', padx=24, pady=(0, 0))
        entry_usuario = tk.Entry(modal, font=("Segoe UI", 12))
        entry_usuario.pack(fill='x', padx=24, pady=(0, 8))
        tk.Label(modal, text="Senha:", font=("Segoe UI", 12), bg='#f6faff').pack(anchor='w', padx=24, pady=(0, 0))
        entry_senha = tk.Entry(modal, font=("Segoe UI", 12), show='*')
        entry_senha.pack(fill='x', padx=24, pady=(0, 8))
        tk.Label(modal, text="Cargo:", font=("Segoe UI", 12), bg='#f6faff').pack(anchor='w', padx=24, pady=(0, 0))
        from servicos.servico_funcionarios import inicializar_cargos
        inicializar_cargos()
        cargos = ['Gerente', 'Vendedor', 'Repositor']
        cargo_var = tk.StringVar()
        cargo_cb = ttk.Combobox(modal, values=cargos, textvariable=cargo_var, font=("Segoe UI", 12), state="readonly")
        cargo_cb.pack(fill='x', padx=24, pady=(0, 8))
        cargo_cb.set("Selecione o cargo")
        def confirmar():
            from servicos.servico_funcionarios import cadastrar_funcionario
            nome = entry_nome.get().strip()
            usuario = entry_usuario.get().strip()
            senha = entry_senha.get().strip()
            cargo = cargo_var.get()
            if not nome or not usuario or not senha or cargo == "Selecione o cargo":
                tk.messagebox.showerror("Erro", "Preencha todos os campos.", parent=modal)
                return
            try:
                cadastrar_funcionario(nome, usuario, senha, cargo)
                tk.messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!", parent=modal)
                modal.destroy()
                self.atualizar_lista_funcionarios()
                if self.atualizar_todas_listas:
                    self.atualizar_todas_listas()
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Erro ao cadastrar funcionário: {e}", parent=modal)
        tk.Button(modal, text="Cadastrar", command=confirmar, bg="#22c55e", fg="white", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, cursor="hand2").pack(pady=(18, 0), ipadx=12, ipady=6)
        tk.Button(modal, text="Cancelar", command=modal.destroy, bg="#e3e8ee", fg="#23272b", font=("Segoe UI", 11), relief=tk.FLAT, cursor="hand2").pack(pady=(8, 0), ipadx=8, ipady=4)

    def abrir_modal_editar(self, funcionario_id):
        # Modal de edição de funcionário
        from servicos.servico_funcionarios import listar_funcionarios, editar_funcionario
        funcionario = next((f for f in listar_funcionarios() if f['id'] == funcionario_id), None)
        if not funcionario:
            tk.messagebox.showerror("Erro", "Funcionário não encontrado.")
            return
        modal = tk.Toplevel(self)
        modal.title("Editar Funcionário")
        modal.geometry("400x350")
        modal.configure(bg='#f6faff')
        modal.transient(self)
        modal.grab_set()
        tk.Label(modal, text="Nome:", font=("Segoe UI", 12), bg='#f6faff').pack(anchor='w', padx=24, pady=(18, 0))
        entry_nome = tk.Entry(modal, font=("Segoe UI", 12))
        entry_nome.insert(0, funcionario.get('nome', ''))
        entry_nome.pack(fill='x', padx=24, pady=(0, 8))
        tk.Label(modal, text="Usuário:", font=("Segoe UI", 12), bg='#f6faff').pack(anchor='w', padx=24, pady=(0, 0))
        entry_usuario = tk.Entry(modal, font=("Segoe UI", 12))
        entry_usuario.insert(0, funcionario.get('usuario', ''))
        entry_usuario.pack(fill='x', padx=24, pady=(0, 8))
        tk.Label(modal, text="Senha (deixe em branco para não alterar):", font=("Segoe UI", 12), bg='#f6faff').pack(anchor='w', padx=24, pady=(0, 0))
        entry_senha = tk.Entry(modal, font=("Segoe UI", 12), show='*')
        entry_senha.pack(fill='x', padx=24, pady=(0, 8))
        tk.Label(modal, text="Cargo:", font=("Segoe UI", 12), bg='#f6faff').pack(anchor='w', padx=24, pady=(0, 0))
        cargos = ['Gerente', 'Vendedor', 'Repositor']
        cargo_var = tk.StringVar()
        cargo_cb = ttk.Combobox(modal, values=cargos, textvariable=cargo_var, font=("Segoe UI", 12), state="readonly")
        cargo_cb.pack(fill='x', padx=24, pady=(0, 8))
        cargo_cb.set(funcionario.get('cargo', 'Selecione o cargo'))
        def confirmar():
            nome = entry_nome.get().strip()
            usuario = entry_usuario.get().strip()
            senha = entry_senha.get().strip()
            cargo = cargo_var.get()
            if not nome or not usuario or cargo == "Selecione o cargo":
                tk.messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.", parent=modal)
                return
            try:
                editar_funcionario(funcionario_id, nome, usuario, senha, cargo)
                tk.messagebox.showinfo("Sucesso", "Funcionário editado com sucesso!", parent=modal)
                modal.destroy()
                self.atualizar_lista_funcionarios()
                if self.atualizar_todas_listas:
                    self.atualizar_todas_listas()
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Erro ao editar funcionário: {e}", parent=modal)
        tk.Button(modal, text="Salvar Alterações", command=confirmar, bg="#2563eb", fg="white", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, cursor="hand2").pack(pady=(18, 0), ipadx=12, ipady=6)
        tk.Button(modal, text="Cancelar", command=modal.destroy, bg="#e3e8ee", fg="#23272b", font=("Segoe UI", 11), relief=tk.FLAT, cursor="hand2").pack(pady=(8, 0), ipadx=8, ipady=4)

    def excluir_funcionario(self, funcionario_id):
        if tk.messagebox.askyesno("Excluir Funcionário", "Tem certeza que deseja excluir este funcionário?"):
            from servicos.servico_funcionarios import excluir_funcionario
            try:
                excluir_funcionario(funcionario_id)
                tk.messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
                self.atualizar_lista_funcionarios()
                if self.atualizar_todas_listas:
                    self.atualizar_todas_listas()
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Erro ao excluir funcionário: {e}")

    def atualizar_lista_funcionarios(self):
        self.criar_cards_funcionarios()
