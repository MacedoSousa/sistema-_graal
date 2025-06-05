import tkinter as tk
from tkinter import ttk, messagebox
from telas.constantes import get_cor
from servicos.servico_comandas import listar_comandas_detalhadas, abrir_nova_comanda, excluir_comanda
from telas.tela_adicionar_item_comanda import TelaAdicionarItemComanda

class TelaComandas(tk.Frame):
    def __init__(self, master, atualizar_todas_listas=None):
        super().__init__(master, bg='#f6faff')
        self.atualizar_todas_listas = atualizar_todas_listas
        self.comandas_feedback_var = tk.StringVar()
        self.comandas_feedback_label = tk.Label(self, textvariable=self.comandas_feedback_var, font=("Segoe UI", 11, "bold"), bg='#f6faff', fg='#e53e3e')
        self.comandas_feedback_label.pack(fill='x', padx=32, pady=(8, 0))
        self.comandas_feedback_label.pack_forget()
        self.criar_card_comandas()

    def criar_card_comandas(self):
        cabecalho_frame = tk.Frame(self, bg=get_cor("cabecalho"))
        cabecalho_frame.pack(fill='x')
        titulo = tk.Label(cabecalho_frame, text="Comandas", bg=get_cor("cabecalho"), fg="white", font=("Segoe UI", 16, "bold"))
        titulo.pack(side='left', padx=10, pady=10)
        botao_adicionar = tk.Button(
            cabecalho_frame,
            text="Nova Comanda",
            command=self.abrir_modal_nova_comanda,
            bg="#2563eb",
            activebackground="#1d4ed8",
            fg="white",
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        botao_adicionar.pack(side='right', padx=10, pady=10)
        self.cards_frame = tk.Frame(self, bg='#f6faff')
        self.cards_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.atualizar_lista_comandas()

    def atualizar_lista_comandas(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        comandas = listar_comandas_detalhadas()
        if not comandas:
            self.comandas_feedback_var.set("Nenhuma comanda aberta.")
            self.comandas_feedback_label.pack(fill='x', padx=32, pady=(8, 0))
            return
        else:
            self.comandas_feedback_label.pack_forget()
        for c in comandas:
            card = tk.Frame(self.cards_frame, bg='white', highlightbackground='#e3e8ee', highlightthickness=2, bd=0)
            card.pack(fill='x', pady=8, padx=0)
            header = tk.Frame(card, bg='white')
            header.pack(fill='x', pady=(8, 0))
            tk.Label(header, text=f"Comanda #{c['id']}", font=("Segoe UI", 14, "bold"), bg='white', fg='#2563eb').pack(side='left', padx=(12, 0))
            tk.Label(header, text=f"Status: {c['status'].capitalize()}", font=("Segoe UI", 11), bg='white', fg='#6b7280').pack(side='left', padx=(18, 0))
            tk.Label(header, text=f"Total: R$ {c['total']:.2f}", font=("Segoe UI", 13, "bold"), bg='white', fg='#22c55e').pack(side='right', padx=(0, 18))
            produtos_frame = tk.Frame(card, bg='white')
            produtos_frame.pack(fill='x', padx=18, pady=(4, 0))
            if c['itens']:
                for item in c['itens']:
                    tk.Label(produtos_frame, text=f"- {item['produto_nome']} x{item['quantidade']} (R$ {item['preco_unitario']:.2f} un)", font=("Segoe UI", 11), bg='white', fg='#23272b').pack(anchor='w')
            else:
                tk.Label(produtos_frame, text="Nenhum produto adicionado", font=("Segoe UI", 11, "italic"), bg='white', fg='#6b7280').pack(anchor='w')
            acoes = tk.Frame(card, bg='white')
            acoes.pack(fill='x', pady=(8, 10), padx=18)
            btn_add = tk.Button(acoes, text="Adicionar Produto", bg="#2563eb", fg="white", font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2", command=lambda cid=c['id']: self.abrir_modal_adicionar_produtos(cid))
            btn_add.pack(side='left', ipadx=8, ipady=3)
            btn_excluir = tk.Button(acoes, text="Excluir Comanda", bg="#e53e3e", fg="white", font=("Segoe UI", 11), relief=tk.FLAT, cursor="hand2", command=lambda cid=c['id']: self.excluir_comanda(cid))
            btn_excluir.pack(side='right', ipadx=8, ipady=3)

    def abrir_modal_nova_comanda(self):
        try:
            comanda_id = abrir_nova_comanda()
            self.atualizar_lista_comandas()
            if self.atualizar_todas_listas:
                self.atualizar_todas_listas()
            messagebox.showinfo("Sucesso", "Comanda aberta com sucesso!")
            self.abrir_modal_adicionar_produtos(comanda_id)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir comanda: {e}")

    def abrir_modal_adicionar_produtos(self, comanda_id):
        def atualizar():
            self.atualizar_lista_comandas()
            if self.atualizar_todas_listas:
                self.atualizar_todas_listas()
        TelaAdicionarItemComanda(self, comanda_id, on_item_added=atualizar)

    def excluir_comanda(self, comanda_id):
        if messagebox.askyesno("Excluir Comanda", f"Tem certeza que deseja excluir a comanda #{comanda_id}?"):
            try:
                excluir_comanda(comanda_id)
                self.atualizar_lista_comandas()
                if self.atualizar_todas_listas:
                    self.atualizar_todas_listas()
                messagebox.showinfo("Sucesso", "Comanda excluída com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir comanda: {e}")
