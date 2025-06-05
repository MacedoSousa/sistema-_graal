import tkinter as tk
from tkinter import ttk, messagebox
from servicos.servico_comandas import abrir_nova_comanda
from telas.tela_adicionar_item_comanda import TelaAdicionarItemComanda

class TelaComandas(ttk.Frame):
    def __init__(self, master, conn):
        super().__init__(master)
        self.conn = conn
        self.master = master

        self.abrir_comanda_button = ttk.Button(
            self, text="Abrir Nova Comanda", bootstyle="warning", command=self.abrir_nova_comanda_ui, width=22
        )
        self.abrir_comanda_button.pack(pady=15)

        self.listagem_frame = ttk.LabelFrame(self, text="Comandas Abertas", bootstyle="primary", padding=15)
        self.treeview_comandas = ttk.Treeview(
            self.listagem_frame,
            columns=("Numero", "Status", "Total", "Itens"),
            show="headings",
            height=8
        )

        self.treeview_comandas.heading("Numero", text="Número")
        self.treeview_comandas.heading("Status", text="Status")
        self.treeview_comandas.heading("Total", text="Total (R$)")
        self.treeview_comandas.heading("Itens", text="Itens")

        self.treeview_comandas.column("Numero", width=90)
        self.treeview_comandas.column("Status", width=110)
        self.treeview_comandas.column("Total", width=110)
        self.treeview_comandas.column("Itens", width=90)

        self.treeview_comandas.bind("<Double-1>", self.selecionar_comanda)
        self.treeview_comandas.pack(fill="both", expand=True)
        self.listagem_frame.pack(pady=10, padx=30, fill="both", expand=True)

        self.frame_acoes = ttk.Frame(self)
        self.frame_acoes.pack(pady=10)
        btn_excluir = ttk.Button(self.frame_acoes, text="Excluir Comanda", bootstyle="danger", command=self.excluir_comanda, width=18)
        btn_excluir.pack(side="left", padx=8)
        btn_atualizar = ttk.Button(self.frame_acoes, text="Atualizar Lista", bootstyle="info", command=self.atualizar_listagem_comandas, width=18)
        btn_atualizar.pack(side="left", padx=8)

        self.atualizar_listagem_comandas()

    def abrir_nova_comanda_ui(self):
        from servicos.servico_produtos import obter_total_de_produtos

        if obter_total_de_produtos() == 0:
            messagebox.showerror(
                "Erro", "Cadastre ao menos um produto antes de abrir uma comanda."
            )
            return
        numero_comanda = abrir_nova_comanda()
        if numero_comanda:
            messagebox.showinfo(
                "Nova Comanda", f"Comanda número {numero_comanda} aberta."
            )
            self.atualizar_listagem_comandas()
            if hasattr(self.master, 'atualizar_comandas_e_recibo'):
                self.master.atualizar_comandas_e_recibo()
        else:
            messagebox.showerror("Erro", "Não foi possível abrir nova comanda.")

    def atualizar_listagem_comandas(self):
        from servicos.servico_comandas import obter_comandas_abertas

        comandas_abertas_data = obter_comandas_abertas()
        self.treeview_comandas.delete(*self.treeview_comandas.get_children())
        for numero_comanda, itens in comandas_abertas_data.items():
            status = "Aberta"
            total = (
                sum(
                    (item["preco_unitario"] or 0) * (item["quantidade"] or 0)
                    for item in itens
                    if item["preco_unitario"] is not None and item["quantidade"] is not None
                )
                if itens
                else 0.0
            )
            self.treeview_comandas.insert(
                "", "end", values=(numero_comanda, status, f"{total:.2f}", len(itens))
            )

    def selecionar_comanda(self, event):
        selecionados = self.treeview_comandas.selection()
        if selecionados:
            item_id = selecionados[0]
            numero_comanda = self.treeview_comandas.item(item_id, 'values')[0]
            win = tk.Toplevel(self)
            win.title(f"Comanda {numero_comanda}")
            try:
                tela = TelaAdicionarItemComanda(win, numero_comanda=numero_comanda)
                tela.pack(fill="both", expand=True)
                win.transient(self.winfo_toplevel())
                win.focus_force()
                win.update_idletasks() 
                win.grab_set()
                win.wait_window() 
            except Exception as e:
                win.destroy()
                messagebox.showerror("Erro", f"Erro ao abrir comanda: {e}")
        else:
            messagebox.showerror("Erro", "Selecione uma comanda.")

    def excluir_comanda(self):
        selecionados = self.treeview_comandas.selection()
        if not selecionados:
            messagebox.showerror("Erro", "Selecione uma comanda para excluir.")
            return
        item_id = selecionados[0]
        numero_comanda = self.treeview_comandas.item(item_id, 'values')[0]
        if messagebox.askyesno("Confirmação", f"Deseja excluir a comanda {numero_comanda}?"):
            from servicos.servico_comandas import excluir_comanda
            if excluir_comanda(numero_comanda):
                self.atualizar_listagem_comandas()
                messagebox.showinfo("Sucesso", "Comanda excluída com sucesso.")
                self.abrir_nova_comanda_ui()
                if hasattr(self.master, 'atualizar_comandas_e_recibo'):
                    self.master.atualizar_comandas_e_recibo()
            else:
                messagebox.showerror("Erro", "Não foi possível excluir a comanda.")

    def on_show(self):
        self.atualizar_listagem_comandas()
        if hasattr(self.master, 'atualizar_comandas_e_recibo'):
            self.master.atualizar_comandas_e_recibo()
