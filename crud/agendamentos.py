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
    janela.geometry("800x600")
    janela.title("Gerenciamento de Agendamentos")
    janela.configure(fg_color="#ECF0F1")
    janela.resizable(False, False)

    frame_campos = ctk.CTkFrame(janela, fg_color="#FFFFFF", corner_radius=10)
    frame_campos.pack(pady=20, padx=20, fill="x")

    label_font = ("Inter", 12)
    entry_font = ("Inter", 12)
    text_color = "#2C3E50"

    ctk.CTkLabel(frame_campos, text="ID (para editar/excluir):", font=label_font, text_color=text_color).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    entrada_id = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_id.grid(row=0, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="ID Animal:", font=label_font, text_color=text_color).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    entrada_animal_id = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_animal_id.grid(row=1, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="ID Serviço:", font=label_font, text_color=text_color).grid(row=2, column=0, padx=10, pady=8, sticky="w")
    entrada_servico_id = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_servico_id.grid(row=2, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Data (AAAA-MM-DD HH:MM):", font=label_font, text_color=text_color).grid(row=3, column=0, padx=10, pady=8, sticky="w")
    entrada_data = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_data.grid(row=3, column=1, padx=10, pady=8)
    
    frame_campos.grid_columnconfigure(0, weight=1)
    frame_campos.grid_columnconfigure(1, weight=3)

    def cadastrar():
        try:
            cadastrar_agendamento(
                entrada_animal_id.get(),
                entrada_servico_id.get(),
                entrada_data.get(),
                ""
            )
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def atualizar():
        try:
            atualizar_agendamento(
                int(entrada_id.get()),
                int(entrada_animal_id.get()),
                int(entrada_servico_id.get()),
                entrada_data.get(),
                "",
                "concluído"
            )
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def excluir():
        try:
            excluir_agendamento(int(entrada_id.get()))
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass
    
    def limpar_campos():
        entrada_id.delete(0, 'end')
        entrada_animal_id.delete(0, 'end')
        entrada_servico_id.delete(0, 'end')
        entrada_data.delete(0, 'end')

    frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
    frame_botoes.pack(pady=10)

    button_font = ("Inter", 12, "bold")
    button_corner_radius = 8

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar, font=button_font, corner_radius=button_corner_radius, fg_color="#3498DB", hover_color="#2980B9").pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Atualizar", command=atualizar, font=button_font, corner_radius=button_corner_radius, fg_color="#3498DB", hover_color="#2980B9").pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Excluir", command=excluir, font=button_font, corner_radius=button_corner_radius, fg_color="#E74C3C", hover_color="#C0392B").pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Limpar", command=limpar_campos, font=button_font, corner_radius=button_corner_radius, fg_color="#95A5A6", hover_color="#7F8C8D").pack(side="left", padx=5)

    frame_lista = ctk.CTkFrame(janela, fg_color="#FFFFFF", corner_radius=10)
    frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

    lista_agendamentos = ctk.CTkTextbox(frame_lista, fg_color="transparent", font=("Inter", 12), text_color="#333333")
    lista_agendamentos.pack(fill="both", expand=True, padx=10, pady=10)

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