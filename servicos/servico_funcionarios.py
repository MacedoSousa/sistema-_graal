import sqlite3
from hashlib import sha256
from servicos.utils import logar_erro

DB_PATH = 'graal.db'

def autenticar(usuario, senha):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    senha_hash = sha256(senha.encode()).hexdigest()
    cur.execute('''
        SELECT funcionario.id_funcionario, funcionario.nome, cargo.nome
        FROM funcionario
        JOIN cargo ON funcionario.id_cargo = cargo.id_cargo
        WHERE funcionario.usuario = ? AND funcionario.senha = ?
    ''', (usuario, senha_hash))
    resultado = cur.fetchone()
    conn.close()
    if resultado:
        return {'id': resultado[0], 'nome': resultado[1], 'cargo': resultado[2]}
    return None

def cadastrar_funcionario(nome, usuario, senha, cargo_nome):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        senha_hash = sha256(senha.encode()).hexdigest()
        cur.execute('SELECT id_cargo FROM cargo WHERE nome = ?', (cargo_nome,))
        cargo = cur.fetchone()
        if not cargo:
            raise Exception('Cargo não encontrado')
        cur.execute('''
            INSERT INTO funcionario (nome, usuario, senha, id_cargo)
            VALUES (?, ?, ?, ?)
        ''', (nome, usuario, senha_hash, cargo[0]))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception('Usuário já existe')
    except Exception as e:
        logar_erro(e)
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def inicializar_cargos():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cargos = ['Gerente', 'Vendedor', 'Repositor']
    for cargo in cargos:
        cur.execute('INSERT OR IGNORE INTO cargo (nome) VALUES (?)', (cargo,))
    conn.commit()
    conn.close()

def listar_funcionarios():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
            SELECT funcionario.id_funcionario, funcionario.nome, funcionario.usuario, cargo.nome
            FROM funcionario
            JOIN cargo ON funcionario.id_cargo = cargo.id_cargo
            ORDER BY funcionario.nome
        ''')
        funcionarios = cur.fetchall()
        return [
            {
                'id': row[0],
                'nome': row[1],
                'usuario': row[2],
                'cargo': row[3]
            } for row in funcionarios
        ]
    except Exception as e:
        logar_erro(e)
        return []
    finally:
        if 'conn' in locals():
            conn.close()
