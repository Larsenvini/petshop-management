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

def atualizar_animal(id_animal, nome, especie, raca, idade, peso):
    executar_query('''
        UPDATE animais 
        SET nome = ?, especie = ?, raca = ?, idade = ?, peso = ?
        WHERE id = ?
    ''', (nome, especie, raca, idade, peso, id_animal))

def excluir_animal(id_animal):
    executar_query('DELETE FROM animais WHERE id = ?', (id_animal,))

def criar_janela_animais():
    janela = ctk.CTk()
    janela.geometry("800x600")
    janela.title("Gerenciamento de Animais")
    janela.configure(fg_color="#FFEADF")

    # Campos de entrada
    frame_campos = ctk.CTkFrame(janela, fg_color="#D9D9D9")
    frame_campos.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(frame_campos, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entrada_nome = ctk.CTkEntry(frame_campos)
    entrada_nome.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Espécie:").grid(row=1, column=0, padx=5, pady=5)
    entrada_especie = ctk.CTkEntry(frame_campos)
    entrada_especie.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Raça:").grid(row=2, column=0, padx=5, pady=5)
    entrada_raca = ctk.CTkEntry(frame_campos)
    entrada_raca.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Idade:").grid(row=3, column=0, padx=5, pady=5)
    entrada_idade = ctk.CTkEntry(frame_campos)
    entrada_idade.grid(row=3, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Peso:").grid(row=4, column=0, padx=5, pady=5)
    entrada_peso = ctk.CTkEntry(frame_campos)
    entrada_peso.grid(row=4, column=1, padx=5, pady=5)

    # Lista de tutores
    frame_tutores = ctk.CTkFrame(frame_campos, fg_color="#D9D9D9")
    frame_tutores.grid(row=5, column=0, columnspan=2, pady=10)

    ctk.CTkLabel(frame_tutores, text="Tutor:").pack(side="left", padx=5)
    lista_tutores = ctk.CTkComboBox(frame_tutores)
    lista_tutores.pack(side="left", padx=5)

    # Botões
    frame_botoes = ctk.CTkFrame(janela, fg_color="#D9D9D9")
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=lambda: cadastrar_animal(
        entrada_nome.get(),
        entrada_especie.get(),
        entrada_raca.get(),
        entrada_idade.get(),
        entrada_peso.get(),
        lista_tutores.get()
    )).pack(side="left", padx=5)

    ctk.CTkButton(frame_botoes, text="Atualizar", command=lambda: atualizar_animal(
        entrada_id.get(),
        entrada_nome.get(),
        entrada_especie.get(),
        entrada_raca.get(),
        entrada_idade.get(),
        entrada_peso.get()
    )).pack(side="left", padx=5)

    ctk.CTkButton(frame_botoes, text="Excluir", command=lambda: excluir_animal(entrada_id.get())).pack(side="left", padx=5)

    # Lista de animais
    frame_lista = ctk.CTkFrame(janela, fg_color="#D9D9D9")
    frame_lista.pack(fill="both", expand=True, padx=20, pady=20)

    lista_animais = ctk.CTkTextbox(frame_lista)
    lista_animais.pack(fill="both", expand=True)

    # Função para atualizar lista
    def atualizar_lista():
        animais = listar_animais()
        lista_animais.delete("1.0", "end")
        for animal in animais:
            lista_animais.insert("end", f"ID: {animal[0]} - {animal[1]} ({animal[2]}) - Tutor: {animal[6]}\n")

    atualizar_lista()

    janela.mainloop()

if __name__ == "__main__":
    criar_tabela_animais()
    criar_janela_animais()
