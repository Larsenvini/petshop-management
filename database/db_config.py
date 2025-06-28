import sqlite3
from sqlite3 import Error

def criar_conexao():
    conn = None
    try:
        conn = sqlite3.connect('database/petshop.db')
        print("Conexão estabelecida com sucesso!")
    except Error as e:
        print(f"Erro na conexão: {e}")
    return conn

def executar_query(query, params=()):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def executar_select(query, params=()):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado
