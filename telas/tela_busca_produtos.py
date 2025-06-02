import tkinter as tk
from tkinter import ttk, messagebox
from telas.tela_base import TelaBase
from servicos.servico_produtos import obter_todos_os_produtos_dict

class TelaBuscaProdutos(tk.Toplevel):
    def __init__(self, master=None, callback_selecionar_produto=None, solicitar_quantidade=False):
        super().__init__(master)
        self.title("Buscar Produtos")
        self.transient(master)

        self.callback_selecionar_produto = callback_selecionar_produto
        self.solicitar_quantidade = solicitar_quantidade
        self.produtos = obter_todos_os_produtos_dict()

        self.treeview_produtos = ttk.Treeview(self, columns=("Codigo", "Nome", "Preco"), show="headings")
        self.treeview_produtos.heading("Codigo", text="Código")
        self.treeview_produtos.heading("Nome", text="Nome")
        self.treeview_produtos.heading("Preco", text="Preço (R$)")

        self.treeview_produtos.column("Codigo", width=80)
        self.treeview_produtos.column("Nome", width=150)
        self.treeview_produtos.column("Preco", width=100)

        if self.produtos:  
            for produto in self.produtos:
                self.treeview_produtos.insert("", "end", values=(produto['id_produto'], produto['nome'], f"{produto['preco']:.2f}"))

        self.treeview_produtos.pack(fill="both", expand=True, padx=10, pady=10)

        frame_baixo = ttk.Frame(self)
        frame_baixo.pack(pady=10)

        if self.solicitar_quantidade:
            ttk.Label(frame_baixo, text="Quantidade:", font=("Arial", 12)).pack(side="left", padx=5)
            self.quantidade_entry = ttk.Entry(frame_baixo, width=8, font=("Arial", 12))
            self.quantidade_entry.pack(side="left", padx=5)
            self.quantidade_entry.insert(0, "1")
        else:
            self.quantidade_entry = None

        self.button_selecionar = ttk.Button(frame_baixo, text="Selecionar Produto", command=self.selecionar_produto)
        self.button_selecionar.pack(side="left", padx=8)

        self.treeview_produtos.bind("<Double-1>", lambda e: self.selecionar_produto())

    def selecionar_produto(self):
        selecionados = self.treeview_produtos.selection()
        if selecionados:
            item_id = selecionados[0]
            codigo_produto = self.treeview_produtos.item(item_id, 'values')[0]
            quantidade = 1
            if self.quantidade_entry:
                try:
                    quantidade = int(self.quantidade_entry.get())
                    if quantidade <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Erro", "Quantidade inválida.")
                    return
            if self.callback_selecionar_produto:
                self.callback_selecionar_produto(codigo_produto, quantidade)
            self.destroy()
        else:
            messagebox.showerror("Erro", "Por favor, selecione um produto.")

if __name__ == "__main__":
    root = tk.Tk()
    tela = TelaBuscaProdutos(root, callback_selecionar_produto=lambda codigo: print(f"Produto selecionado: {codigo}"))
    tela.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
