import customtkinter as ctk
from database.db_config import criar_conexao, executar_query, executar_select

def criar_tabela_animais():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especie TEXT NOT NULL,
            raca TEXT,
            idade INTEGER,
            peso REAL,
            id_tutor INTEGER,
            FOREIGN KEY (id_tutor) REFERENCES tutores(id)
        )
    ''')
    conn.close()

def cadastrar_animal(nome, especie, raca, idade, peso, id_tutor):
    executar_query('''
        INSERT INTO animais (nome, especie, raca, idade, peso, id_tutor)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, especie, raca, idade, peso, id_tutor))

def listar_animais():
    return executar_select('''
        SELECT a.*, t.nome as nome_tutor 
        FROM animais a
        JOIN tutores t ON a.id_tutor = t.id
    ''')

def atualizar_animal(id_animal, nome, especie, raca, idade, peso, id_tutor):
    executar_query('''
        UPDATE animais 
        SET nome = ?, especie = ?, raca = ?, idade = ?, peso = ?, id_tutor = ?
        WHERE id = ?
    ''', (nome, especie, raca, idade, peso, id_tutor, id_animal))

def excluir_animal(id_animal):
    executar_query('DELETE FROM animais WHERE id = ?', (id_animal,))

def obter_tutores():
    return executar_select('SELECT id, nome FROM tutores')

def criar_janela_animais():
    janela = ctk.CTk()
    janela.geometry("800x600")
    janela.title("Gerenciamento de Animais")
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

    ctk.CTkLabel(frame_campos, text="Nome:", font=label_font, text_color=text_color).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    entrada_nome = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_nome.grid(row=1, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Espécie:", font=label_font, text_color=text_color).grid(row=2, column=0, padx=10, pady=8, sticky="w")
    entrada_especie = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_especie.grid(row=2, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Raça:", font=label_font, text_color=text_color).grid(row=3, column=0, padx=10, pady=8, sticky="w")
    entrada_raca = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_raca.grid(row=3, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Idade:", font=label_font, text_color=text_color).grid(row=4, column=0, padx=10, pady=8, sticky="w")
    entrada_idade = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_idade.grid(row=4, column=1, padx=10, pady=8)
    
    ctk.CTkLabel(frame_campos, text="Peso:", font=label_font, text_color=text_color).grid(row=5, column=0, padx=10, pady=8, sticky="w")
    entrada_peso = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_peso.grid(row=5, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="ID do Tutor:", font=label_font, text_color=text_color).grid(row=6, column=0, padx=10, pady=8, sticky="w")
    entrada_tutor_id = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_tutor_id.grid(row=6, column=1, padx=10, pady=8)

    frame_campos.grid_columnconfigure(0, weight=1)
    frame_campos.grid_columnconfigure(1, weight=3)
    
    def cadastrar():
        try:
            cadastrar_animal(
                entrada_nome.get(),
                entrada_especie.get(),
                entrada_raca.get(),
                int(entrada_idade.get()),
                int(entrada_peso.get()),
                int(entrada_tutor_id.get())
            )
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def atualizar():
        try:
            atualizar_animal(
                int(entrada_id.get()),
                entrada_nome.get(),
                entrada_especie.get(),
                entrada_raca.get(),
                int(entrada_idade.get()),
                int(entrada_tutor_id.get())
            )
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def excluir():
        try:
            excluir_animal(int(entrada_id.get()))
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def limpar_campos():
        entrada_id.delete(0, 'end')
        entrada_nome.delete(0, 'end')
        entrada_especie.delete(0, 'end')
        entrada_raca.delete(0, 'end')
        entrada_idade.delete(0, 'end')
        entrada_tutor_id.delete(0, 'end')

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

    lista_animais = ctk.CTkTextbox(frame_lista, fg_color="transparent", font=("Inter", 12), text_color="#333333")
    lista_animais.pack(fill="both", expand=True, padx=10, pady=10)

    def atualizar_lista():
        animais = listar_animais()
        lista_animais.delete("1.0", "end")
        for animal in animais:
            lista_animais.insert("end", f"ID: {animal[0]} - {animal[1]} ({animal[2]}) - Tutor: {animal[7]}\n")

    atualizar_lista()
    janela.mainloop()

if __name__ == "__main__":
    criar_tabela_animais()
    criar_janela_animais()