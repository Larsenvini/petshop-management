import customtkinter as ctk
from database.db_config import criar_conexao, executar_query, executar_select

def criar_tabela_pagamentos():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_agendamento INTEGER NOT NULL,
            valor REAL NOT NULL,
            forma_pagamento TEXT NOT NULL,
            status TEXT DEFAULT 'pendente',
            data_pagamento DATETIME,
            FOREIGN KEY (id_agendamento) REFERENCES agendamentos(id)
        )
    ''')
    conn.close()

def cadastrar_pagamento(id_agendamento, valor, forma_pagamento):
    executar_query('''
        INSERT INTO pagamentos (id_agendamento, valor, forma_pagamento)
        VALUES (?, ?, ?)
    ''', (id_agendamento, valor, forma_pagamento))

def listar_pagamentos():
    return executar_select('''
        SELECT p.*, a.data_hora, s.nome as nome_servico, ani.nome as nome_animal, t.nome as nome_tutor 
        FROM pagamentos p
        JOIN agendamentos a ON p.id_agendamento = a.id
        JOIN servicos s ON a.id_servico = s.id
        JOIN animais ani ON a.id_animal = ani.id
        JOIN tutores t ON ani.id_tutor = t.id
    ''')

def atualizar_pagamento(id_pagamento, valor, forma_pagamento, status, data_pagamento):
    executar_query('''
        UPDATE pagamentos 
        SET valor = ?, forma_pagamento = ?, status = ?, data_pagamento = ?
        WHERE id = ?
    ''', (valor, forma_pagamento, status, data_pagamento, id_pagamento))

def excluir_pagamento(id_pagamento):
    executar_query('DELETE FROM pagamentos WHERE id = ?', (id_pagamento,))

def criar_janela_pagamentos():
    janela = ctk.CTk()
    janela.geometry("1000x700")
    janela.title("Gerenciamento de Pagamentos")
    janela.configure(fg_color="#3179a2")

    # Campos de entrada
    frame_campos = ctk.CTkFrame(janela, fg_color="#FFFFFF")
    frame_campos.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(frame_campos, text="Agendamento:").grid(row=0, column=0, padx=5, pady=5)
    lista_agendamentos = ctk.CTkComboBox(frame_campos)
    lista_agendamentos.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Valor:").grid(row=1, column=0, padx=5, pady=5)
    entrada_valor = ctk.CTkEntry(frame_campos)
    entrada_valor.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Forma de Pagamento:").grid(row=2, column=0, padx=5, pady=5)
    lista_formas = ctk.CTkComboBox(frame_campos)
    lista_formas.grid(row=2, column=1, padx=5, pady=5)

    # Botões
    frame_botoes = ctk.CTkFrame(janela, fg_color="#3179a2")
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=lambda: cadastrar_pagamento(
        lista_agendamentos.get(),
        entrada_valor.get(),
        lista_formas.get()
    )).pack(side="left", padx=5)

    ctk.CTkButton(frame_botoes, text="Atualizar", command=lambda: atualizar_pagamento(
        entrada_id.get(),
        entrada_valor.get(),
        lista_formas.get(),
        lista_status.get(),
        entrada_data.get()
    )).pack(side="left", padx=5)

    ctk.CTkButton(frame_botoes, text="Excluir", command=lambda: excluir_pagamento(entrada_id.get())).pack(side="left", padx=5)

    # Lista de pagamentos
    frame_lista = ctk.CTkFrame(janela, fg_color="#3179a2")
    frame_lista.pack(fill="both", expand=True, padx=20, pady=20)

    lista_pagamentos = ctk.CTkTextbox(frame_lista)
    lista_pagamentos.pack(fill="both", expand=True)

    # Função para atualizar lista
    def atualizar_lista():
        pagamentos = listar_pagamentos()
        lista_pagamentos.delete("1.0", "end")
        for pagamento in pagamentos:
            lista_pagamentos.insert("end", f"ID: {pagamento[0]} - R${pagamento[2]:.2f} - {pagamento[3]} - Status: {pagamento[4]}\n")

    atualizar_lista()

    janela.mainloop()

if __name__ == "__main__":
    criar_tabela_pagamentos()
    criar_janela_pagamentos()
