import logging
import re
import sys
import os

logging.basicConfig(filename='sistema.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

def logar_erro(e):
    logging.error(str(e))

def validar_cpf(cpf):
    """Valida se o CPF possui 11 dígitos numéricos."""
    return re.match(r'^\d{11}$', cpf) is not None

def campo_obrigatorio(valor):
    return valor is not None and str(valor).strip() != ''

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def formatar_preco_brasileiro(valor):
    """Formata um número float para o padrão brasileiro: 1.234,56"""
    try:
        return f"{valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except Exception:
        return str(valor)

TEXTOS = {
    'login_sucesso': 'Login realizado com sucesso!',
    'erro_login': 'Usuário ou senha inválidos.',
    'erro_campo_obrigatorio': 'Preencha todos os campos.',
    'erro_cpf': 'CPF inválido. Digite 11 números.',
    'erro_geral': 'Ocorreu um erro inesperado.',
    'sucesso_cadastro': 'Administrador cadastrado com sucesso!',
    'sucesso_pagamento': 'Pagamento realizado e recibo gerado!',
}
