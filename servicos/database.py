import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "graal.db")
SQL_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "graal.sql")

def banco_existe_e_valido():
    if not os.path.exists(DB_PATH):
        return False
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")
        return True
    except sqlite3.DatabaseError as e:
        print(f"Erro ao verificar a validade do banco de dados: {e}")
        return False

def conectar_banco_de_dados():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco SQLite: {e}")
        return None

def criar_banco():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            with open(SQL_SCRIPT_PATH, "r", encoding="utf-8") as f:
                script = f.read()

            script = script.replace("CREATE DATABASE graal;", "")
            script = script.replace("USE graal;", "")
            
            for command in script.split(";"):
                command = command.strip()
                if command and not command.startswith("--"):
                    try:
                        cursor.execute(command)
                    except Exception as e:
                        print(f"Erro ao executar comando: {command[:80]}\nErro: {e}")

            conn.commit()
        print("Banco criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar banco: {e}")

def inicializar_banco():
    if not banco_existe_e_valido():
        print("Banco inexistente ou inválido. Criando...")
        criar_banco()
    else:
        print("Banco de dados já está configurado e válido.")

def get_connection():
    return sqlite3.connect(DB_PATH)

def fetchone(query, params=None):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params or ())
        return cur.fetchone()

def fetchall(query, params=None):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params or ())
        return cur.fetchall()

def execute(query, params=None):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params or ())
        conn.commit()
