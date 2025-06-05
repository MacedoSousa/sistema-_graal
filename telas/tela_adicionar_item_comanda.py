import tkinter as tk
from tkinter import ttk, messagebox
from servicos.servico_comandas import obter_comanda
from servicos.servico_produtos import obter_produto_por_codigo

class TelaAdicionarItemComanda(tk.Toplevel):
    def __init__(self, master=None, numero_comanda=None, on_item_added=None):
        super().__init__(master)
        self.title("Adicionar Itens à Comanda")
        self.numero_comanda = numero_comanda
        self.on_item_added = on_item_added
        self.geometry("600x400")
        self.configure(bg='#f6faff')
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        titulo = ttk.Label(self, text=f"Adicionar Itens à Comanda", font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(12, 2), sticky="ew")
        label_comanda = ttk.Label(self, text=f"Comanda: {self.numero_comanda}", font=("Arial", 15, "bold"))
        label_comanda.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        self.listagem_frame = ttk.LabelFrame(self, text="Itens da Comanda", padding=10)
        self.listagem_frame.grid(row=2, column=0, columnspan=2, padx=18, pady=8, sticky="nsew")
        self.listagem_frame.grid_columnconfigure(0, weight=1)
        self.treeview_itens = ttk.Treeview(self.listagem_frame, columns=("Nome", "Quantidade", "Preço Unitário", "Subtotal"), show="headings", height=7)
        self.treeview_itens.heading("Nome", text="Nome")
        self.treeview_itens.heading("Quantidade", text="Quantidade")
        self.treeview_itens.heading("Preço Unitário", text="Preço Unitário (R$)")
        self.treeview_itens.heading("Subtotal", text="Subtotal (R$)")
        self.treeview_itens.column("Nome", width=150)
        self.treeview_itens.column("Quantidade", width=100)
        self.treeview_itens.column("Preço Unitário", width=120)
        self.treeview_itens.column("Subtotal", width=120)
        self.treeview_itens.pack(fill="both", expand=True)
        self.atualizar_itens_comanda()

        self.frame_botoes = ttk.Frame(self)
        self.frame_botoes.grid(row=3, column=0, columnspan=2, pady=12)
        self.buscar_produto_button = ttk.Button(self.frame_botoes, text="Adicionar Produto à Comanda", command=self.buscar_produto)
        self.buscar_produto_button.pack(side="left", padx=8)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def buscar_produto(self):
        from servicos.servico_produtos import obter_todos_os_produtos_dict
        produtos = obter_todos_os_produtos_dict()
        top = tk.Toplevel(self)
        top.title("Escolher Produto")
        top.geometry("700x400")
        top.configure(bg='#f6faff')
        top.transient(self)
        top.grab_set()

        canvas = tk.Canvas(top, bg='#f6faff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        frame_cards = tk.Frame(canvas, bg='#f6faff')
        frame_cards.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=frame_cards, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def selecionar(produto):
            def confirmar():
                try:
                    quantidade = int(entry_quantidade.get())
                except Exception:
                    quantidade = 1
                top.destroy()
                self.selecionar_produto_callback(produto['id'], quantidade)
            modal = tk.Toplevel(top)
            modal.title(f"Quantidade - {produto['nome']}")
            modal.geometry("300x150")
            tk.Label(modal, text=f"Produto: {produto['nome']}", font=("Segoe UI", 12, "bold")).pack(pady=(12, 4))
            tk.Label(modal, text=f"Preço: R$ {produto['preco']:.2f}", font=("Segoe UI", 11)).pack()
            tk.Label(modal, text="Quantidade:").pack(pady=(8, 2))
            entry_quantidade = tk.Entry(modal)
            entry_quantidade.insert(0, "1")
            entry_quantidade.pack()
            ttk.Button(modal, text="Adicionar", command=confirmar).pack(pady=10)
            modal.transient(top)
            modal.grab_set()
            self.wait_window(modal)

        for idx, produto in enumerate(produtos):
            card = tk.Frame(frame_cards, bg='white', highlightbackground='#e3e8ee', highlightthickness=2, bd=0)
            card.grid(row=idx//3, column=idx%3, padx=16, pady=16, sticky='n')
            tk.Label(card, text=produto['nome'], font=("Segoe UI", 13, "bold"), bg='white').pack(pady=(8, 0))
            tk.Label(card, text=f"Preço: R$ {produto['preco']:.2f}", font=("Segoe UI", 11), bg='white', fg='#2563eb').pack()
            tk.Label(card, text=f"Estoque: {produto['quantidade']}", font=("Segoe UI", 10), bg='white', fg='#6b7280').pack()
            ttk.Button(card, text="Selecionar", command=lambda p=produto: selecionar(p)).pack(pady=8)

        self.wait_window(top)

    def selecionar_produto_callback(self, codigo_produto, quantidade):
        from servicos.servico_produtos import obter_produto_por_codigo, checar_estoque, atualizar_estoque
        produto = obter_produto_por_codigo(codigo_produto)
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
        if not checar_estoque(produto['id_produto'], quantidade):
            messagebox.showerror("Estoque insuficiente", f"Produto '{produto['nome']}' sem estoque suficiente.")
            return
        try:
            from servicos.servico_comandas import adicionar_item_a_comanda
            adicionar_item_a_comanda(self.numero_comanda, produto, quantidade)
            atualizar_estoque(produto['id_produto'], quantidade)
            messagebox.showinfo("Sucesso", f"{quantidade}x '{produto['nome']}' adicionado à comanda.")
            self.atualizar_itens_comanda()
            if self.on_item_added:
                self.on_item_added()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar item: {e}")

    def atualizar_itens_comanda(self):
        self.comanda = obter_comanda(self.numero_comanda)
        self.treeview_itens.delete(*self.treeview_itens.get_children())
        if self.comanda and self.comanda['itens']:
            for item in self.comanda['itens']:
                subtotal = item['preco_unitario'] * item['quantidade']
                self.treeview_itens.insert("", "end", values=(item['produto_nome'], item['quantidade'], f"{item['preco_unitario']:.2f}", f"{subtotal:.2f}"))

if __name__ == "__main__":
    root = tk.Tk()
    tela = TelaAdicionarItemComanda(root, numero_comanda=1)
    tela.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
