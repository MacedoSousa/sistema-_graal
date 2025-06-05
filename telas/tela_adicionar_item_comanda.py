import tkinter as tk
from tkinter import ttk, messagebox
from telas.tela_base import TelaBase
from servicos.servico_comandas import obter_comanda
from telas.tela_busca_produtos import TelaBuscaProdutos
from servicos.servico_produtos import obter_produto_por_codigo

class TelaAdicionarItemComanda(TelaBase):
    def __init__(self, master=None, numero_comanda=None):
        super().__init__(master, title=None)
        self.master = master
        self.numero_comanda = numero_comanda

        titulo = ttk.Label(self, text=f"Adicionar Itens à Comanda", font=("Arial", 18, "bold"), bootstyle="primary")
        titulo.grid(row=0, column=0, columnspan=2, pady=(12, 2), sticky="ew")
        label_comanda = ttk.Label(self, text=f"Comanda: {self.numero_comanda}", font=("Arial", 15, "bold"), bootstyle="info")
        label_comanda.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        self.listagem_frame = ttk.LabelFrame(self, text="Itens da Comanda", bootstyle="primary", padding=10)
        self.listagem_frame.grid(row=2, column=0, columnspan=2, padx=18, pady=8, sticky="nsew")
        self.listagem_frame.grid_columnconfigure(0, weight=1)
        self.treeview_itens = ttk.Treeview(self.listagem_frame, columns=("ID", "Nome", "Quantidade", "Preço Unitário", "Subtotal"), show="headings", height=7)
        self.treeview_itens.heading("ID", text="ID")
        self.treeview_itens.heading("Nome", text="Nome")
        self.treeview_itens.heading("Quantidade", text="Quantidade")
        self.treeview_itens.heading("Preço Unitário", text="Preço Unitário (R$)")
        self.treeview_itens.heading("Subtotal", text="Subtotal (R$)")
        self.treeview_itens.column("ID", width=0, stretch=False)
        self.treeview_itens.column("Nome", width=150)
        self.treeview_itens.column("Quantidade", width=100)
        self.treeview_itens.column("Preço Unitário", width=120)
        self.treeview_itens.column("Subtotal", width=120)
        self.treeview_itens.pack(fill="both", expand=True)
        self.atualizar_itens_comanda()

        self.frame_botoes = ttk.Frame(self)
        self.frame_botoes.grid(row=3, column=0, columnspan=2, pady=12)
        self.buscar_produto_button = ttk.Button(self.frame_botoes, text="Adicionar Produto à Comanda", bootstyle="success", command=self.buscar_produto)
        self.buscar_produto_button.pack(side="left", padx=8)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def buscar_produto(self):
        busca = TelaBuscaProdutos(self, callback_selecionar_produto=self.selecionar_produto_callback, solicitar_quantidade=True)
        self.wait_window(busca)

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
            if hasattr(self.master, 'master') and hasattr(self.master.master, 'atualizar_comandas_e_recibo'):
                self.master.master.atualizar_comandas_e_recibo()
            if hasattr(self.master, 'master') and hasattr(self.master.master, 'atualizar_produtos_e_inicial'):
                self.master.master.atualizar_produtos_e_inicial()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar item: {e}")

    def atualizar_itens_comanda(self):
        self.comanda = obter_comanda(self.numero_comanda)
        self.treeview_itens.delete(*self.treeview_itens.get_children())
        if self.comanda and self.comanda['itens']:
            for item in self.comanda['itens']:
                subtotal = item['preco_unitario'] * item['quantidade']
                self.treeview_itens.insert("", "end", values=(item.get('id_produto', ''), item['produto_nome'], item['quantidade'], f"{item['preco_unitario']:.2f}", f"{subtotal:.2f}"))

    def buscar_nome_produto(codigo_produto):
        produto = obter_produto_por_codigo(codigo_produto)
        if produto:
            return produto
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    
    tela = TelaAdicionarItemComanda(root, numero_comanda=1)  
    tela.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
