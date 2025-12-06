import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("finanças.db") #defini função conectar 

def criar_tabelas():
    conn = conectar() #conexão com banco
    cur = conn.cursor() #cursor: objeto para executar sql

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )""") #cria tabela com id do usuario,nome,senha e o camo n pode ficar vazio
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transacoes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
                )""") #guarda tudo que o usuario insere com tio,descrição,valor e tbm tem uma relação com users.
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS metas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                objetivo REAL NOT NULL DEFAULT 0,
                progresso REAL NOT NULL DEFAULT 0,
                data_criacao TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
                )""")
    
    conn.commit() # salva as mudanças
    conn.close()  # fecha a conexão

def criar_usuario(username, password):
    conn = conectar()
    cur = conn.cursor()
    #abre conexão com o banco
    try: #comando de inserção, '?' são placeholders evitando sql injection, dando certo retorna true, o usuario que ja existe retorna false, fecha a conexão dando erro ou não
        cur.execute("INSERT INTO users (username,password)  VALUES (?,?)", (username,password)) 
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def validar_login(username, password):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()    #busca nome e senha fornecido, pega o primeiro resultado ou none
    conn.close()
    return user #retorna user se existir,se n none

def inserir_transacao(user_id,tipo,descricao,valor,data):
    conn = conectar()
    cur = conn.cursor()

    if data is None:
        data = datetime.now().strftime("%d-%m-%Y")

    cur.execute("INSERT INTO transacoes (user_id,tipo,descricao,valor,data) VALUES (?,?,?,?,?)",
                (user_id,tipo,descricao,valor,data)) # insere transação, preenchendo user,tio,descrição e valor
    conn.commit()
    conn.close()

def listar_transacoes(user_id, tipo=None):
    conn = conectar()
    cur = conn.cursor()

    if tipo: #filtro or tipo
        cur.execute("SELECT id,user_id,tipo,descricao,valor, data FROM transacoes WHERE user_id = ? AND tipo = ?", (user_id, tipo))
    else:
        cur.execute("SELECT id, user_id,tipo,descricao,valor, data FROM transacoes WHERE user_id = ?", (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows #retorna lista de transacoes

def deletar_transacao(id_transacao): #aaga do banco a transação com id especifico
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM transacoes WHERE id = ?", (id_transacao,))
    conn.commit()
    conn.close()

#metas
def criar_metas(user_id, descricao,objetivo):
    conn = conectar()
    cur = conn.cursor()

    data = datetime.now().strftime("%d-%m-%Y")
    cur.execute("INSERT INTO metas (user_id,descricao,objetivo,progresso, data_criacao) VALUES (?,?,?, 0, ?)", (user_id,descricao,objetivo, data))
    conn.commit()
    conn.close()

def listar_metas(user_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM metas WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def adicionar_progresso(id_meta, valor):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE metas SET progresso = progresso + ? WHERE id = ?", (valor,id_meta))
    conn.commit()
    conn.close()

def deletar_meta(id_meta):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM metas WHERE id= ?", (id_meta,))
    conn.commit()
    conn.close()
