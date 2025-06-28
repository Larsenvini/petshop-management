import sqlite3
import os

DATABASE_PATH = "database/petshop.db"

def criar_conexao():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def executar_query(query, params=None):
    conn = criar_conexao()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()

def executar_select(query, params=None):
    conn = criar_conexao()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def inicializar_banco():
    from crud.tutores import criar_tabela_tutores
    from crud.animais import criar_tabela_animais
    from crud.servicos import criar_tabela_servicos
    from crud.agendamentos import criar_tabela_agendamentos
    from crud.pagamentos import criar_tabela_pagamentos
    
    criar_tabela_tutores()
    criar_tabela_animais()
    criar_tabela_servicos()
    criar_tabela_agendamentos()
    criar_tabela_pagamentos()