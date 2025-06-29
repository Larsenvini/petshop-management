import customtkinter as ctk
from database.db_config import criar_conexao, executar_query, executar_select

def criar_tabela_agendamentos():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_animal INTEGER NOT NULL,
            id_servico INTEGER NOT NULL,
            data_hora DATETIME NOT NULL,
            observacoes TEXT,
            status TEXT DEFAULT 'pendente',
            FOREIGN KEY (id_animal) REFERENCES animais(id),
            FOREIGN KEY (id_servico) REFERENCES servicos(id)
        )
    ''')
    conn.close()

def cadastrar_agendamento(id_animal, id_servico, data_hora, observacoes):
    executar_query('''
        INSERT INTO agendamentos (id_animal, id_servico, data_hora, observacoes)
        VALUES (?, ?, ?, ?)
    ''', (id_animal, id_servico, data_hora, observacoes))

def listar_agendamentos():
    return executar_select('''
        SELECT a.*, s.nome as nome_servico, ani.nome as nome_animal, t.nome as nome_tutor 
        FROM agendamentos a
        JOIN servicos s ON a.id_servico = s.id
        JOIN animais ani ON a.id_animal = ani.id
        JOIN tutores t ON ani.id_tutor = t.id
    ''')

def atualizar_agendamento(id_agendamento, id_animal, id_servico, data_hora, observacoes, status):
    executar_query('''
        UPDATE agendamentos 
        SET id_animal = ?, id_servico = ?, data_hora = ?, observacoes = ?, status = ?
        WHERE id = ?
    ''', (id_animal, id_servico, data_hora, observacoes, status, id_agendamento))

def excluir_agendamento(id_agendamento):
    executar_query('DELETE FROM agendamentos WHERE id = ?', (id_agendamento,))

def criar_janela_agendamentos():
    janela = ctk.CTk()
    janela.geometry("1000x700")
    janela.title("Gerenciamento de Agendamentos")
    janela.configure(fg_color="#3179a2")

    # Campos de entrada
    frame_campos = ctk.CTkFrame(janela, fg_color="#FFFFFF")
    frame_campos.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(frame_campos, text="Animal:").grid(row=0, column=0, padx=5, pady=5)
    lista_animais = ctk.CTkComboBox(frame_campos)
    lista_animais.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Serviço:").grid(row=1, column=0, padx=5, pady=5)
    lista_servicos = ctk.CTkComboBox(frame_campos)
    lista_servicos.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Data e Hora:").grid(row=2, column=0, padx=5, pady=5)
    entrada_data = ctk.CTkEntry(frame_campos)
    entrada_data.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Observações:").grid(row=3, column=0, padx=5, pady=5)
    entrada_observacoes = ctk.CTkEntry(frame_campos)
    entrada_observacoes.grid(row=3, column=1, padx=5, pady=5)

    # Botões
    frame_botoes = ctk.CTkFrame(janela, fg_color="#3179a2")
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=lambda: cadastrar_agendamento(
        lista_animais.get(),
        lista_servicos.get(),
        entrada_data.get(),
        entrada_observacoes.get()
    )).pack(side="left", padx=5)

    ctk.CTkButton(frame_botoes, text="Atualizar", command=lambda: atualizar_agendamento(
        entrada_id.get(),
        lista_animais.get(),
        lista_servicos.get(),
        entrada_data.get(),
        entrada_observacoes.get(),
        lista_status.get()
    )).pack(side="left", padx=5)

    ctk.CTkButton(frame_botoes, text="Excluir", command=lambda: excluir_agendamento(entrada_id.get())).pack(side="left", padx=5)

    # Lista de agendamentos
    frame_lista = ctk.CTkFrame(janela, fg_color="#3179a2")
    frame_lista.pack(fill="both", expand=True, padx=20, pady=20)

    lista_agendamentos = ctk.CTkTextbox(frame_lista)
    lista_agendamentos.pack(fill="both", expand=True)

    # Função para atualizar lista
    def atualizar_lista():
        agendamentos = listar_agendamentos()
        lista_agendamentos.delete("1.0", "end")
        for agendamento in agendamentos:
            lista_agendamentos.insert("end", f"ID: {agendamento[0]} - {agendamento[7]} ({agendamento[8]}) - {agendamento[5]}\n")

    atualizar_lista()

    janela.mainloop()

if __name__ == "__main__":
    criar_tabela_agendamentos()
    criar_janela_agendamentos()
