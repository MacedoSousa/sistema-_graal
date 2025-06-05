import tkinter as tk

TEMA_ESCURO = {
    'fundo_janela': '#232323',
    'fundo_card': '#262626',  # levemente mais escuro para cards
    'texto_titulo': '#F5F5F5',
    'texto_label': '#B0BEC5',
    'input_bg': '#292929',  # zebra mais perceptível
    'input_fg': '#F5F5F5',
    'input_border': '#555555',  # borda mais visível
    'botao_bg': '#232323',
    'botao_fg': '#F5F5F5',
    'label_azul': '#B0BEC5',
    'destaque_vermelho': '#AAAAAA',
    'destaque_verde': '#E0E0E0',
    'icone_vendas': '#B0BEC5',
    'icone_funcionarios': '#B0BEC5',
    'card_shadow': '#181818',
    'card_border': '#555555',
    'card_hover': '#353535',  # hover mais claro
    'card_focus': '#AAAAAA',
    'card_radius': 18,
    'card_shadow_offset': (2, 4),
    'treeview_padding': (6, 2),
}
TEMA_CLARO = {
    'fundo_janela': '#FFFFFF',
    'fundo_card': '#FFFFFF',
    'texto_titulo': '#000000',
    'texto_label': '#000000',
    'input_bg': '#FFFFFF',
    'input_fg': '#000000',
    'input_border': '#BBBBBB',
    'botao_bg': '#FFFFFF',
    'botao_fg': '#000000',
    'label_azul': '#000000',
    'destaque_vermelho': '#000000',
    'destaque_verde': '#000000',
    'icone_vendas': '#000000',
    'icone_funcionarios': '#000000',
    'card_shadow': '#FFFFFF',
    'card_border': '#BBBBBB',
    'card_hover': '#F0F0F0',
    'card_focus': '#888888',
    'card_radius': 18,
    'card_shadow_offset': (2, 4),
    'treeview_padding': (6, 2),
}

FONTE_TITULO = ("Arial", 18, "bold")
FONTE_LABEL = ("Arial", 12, "bold")
FONTE_INPUT = ("Arial", 12)
FONTE_BOTAO = ("Arial", 12, "bold")
FONTE_LOGO = ("Arial", 22, "bold")

TEMA_ATUAL = TEMA_CLARO

def setar_tema(escuro=True):
    global TEMA_ATUAL
    TEMA_ATUAL = TEMA_ESCURO if escuro else TEMA_CLARO

def get_cor(nome):
    return TEMA_ATUAL.get(nome, '#23272b')

def criar_botao_tema(parent, callback=None):
    def alternar():
        escuro = TEMA_ATUAL is not TEMA_ESCURO
        setar_tema(escuro)
        btn.config(text=texto())
        if callback:
            callback()
    def texto():
        return "🌙 Escuro" if TEMA_ATUAL is TEMA_CLARO else "☀️ Claro"
    btn = tk.Button(parent, text=texto(), font=FONTE_BOTAO, bg=get_cor('botao_bg'), fg=get_cor('botao_fg'),
                    relief='flat', bd=0, command=alternar, highlightthickness=0)
    btn.pack(side="right", padx=12, pady=8)
    return btn

def centralizar_janela(janela, largura=None, altura=None):
    janela.update_idletasks()
    if largura is None or altura is None:
        largura = janela.winfo_width()
        altura = janela.winfo_height()
        if largura == 1 or altura == 1:
            # fallback para tamanho default se ainda não renderizou
            largura = 800
            altura = 600
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
