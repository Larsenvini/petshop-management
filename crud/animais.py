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
    janela.configure(fg_color="#FFFFFF")

    frame_campos = ctk.CTkFrame(janela, fg_color="#FFFFFF")
    frame_campos.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(frame_campos, text="ID (para editar/excluir):").grid(row=0, column=0, padx=5, pady=5)
    entrada_id = ctk.CTkEntry(frame_campos)
    entrada_id.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
    entrada_nome = ctk.CTkEntry(frame_campos)
    entrada_nome.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Espécie:").grid(row=2, column=0, padx=5, pady=5)
    entrada_especie = ctk.CTkEntry(frame_campos)
    entrada_especie.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Raça:").grid(row=3, column=0, padx=5, pady=5)
    entrada_raca = ctk.CTkEntry(frame_campos)
    entrada_raca.grid(row=3, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Idade:").grid(row=4, column=0, padx=5, pady=5)
    entrada_idade = ctk.CTkEntry(frame_campos)
    entrada_idade.grid(row=4, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Peso:").grid(row=5, column=0, padx=5, pady=5)
    entrada_peso = ctk.CTkEntry(frame_campos)
    entrada_peso.grid(row=5, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Tutor:").grid(row=6, column=0, padx=5, pady=5)
    lista_tutores = ctk.CTkComboBox(frame_campos)
    lista_tutores.grid(row=6, column=1, padx=5, pady=5)

    def carregar_tutores():
        tutores = obter_tutores()
        valores = [f"{tutor[0]} - {tutor[1]}" for tutor in tutores]
        lista_tutores.configure(values=valores)
        if valores:
            lista_tutores.set(valores[0])

    def cadastrar():
        try:
            tutor_selecionado = lista_tutores.get()
            id_tutor = int(tutor_selecionado.split(" - ")[0])
            cadastrar_animal(
                entrada_nome.get(),
                entrada_especie.get(),
                entrada_raca.get(),
                int(entrada_idade.get()),
                float(entrada_peso.get()),
                id_tutor
            )
            limpar_campos()
            atualizar_lista()
        except (ValueError, IndexError):
            pass

    def atualizar():
        try:
            tutor_selecionado = lista_tutores.get()
            id_tutor = int(tutor_selecionado.split(" - ")[0])
            atualizar_animal(
                int(entrada_id.get()),
                entrada_nome.get(),
                entrada_especie.get(),
                entrada_raca.get(),
                int(entrada_idade.get()),
                float(entrada_peso.get()),
                id_tutor
            )
            limpar_campos()
            atualizar_lista()
        except (ValueError, IndexError):
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
        entrada_peso.delete(0, 'end')

    frame_botoes = ctk.CTkFrame(janela, fg_color="#2196F3")
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Atualizar", command=atualizar).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Excluir", command=excluir).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Limpar", command=limpar_campos).pack(side="left", padx=5)

    frame_lista = ctk.CTkFrame(janela, fg_color="#2196F3")
    frame_lista.pack(fill="both", expand=True, padx=20, pady=20)

    lista_animais = ctk.CTkTextbox(frame_lista)
    lista_animais.pack(fill="both", expand=True)

    def atualizar_lista():
        animais = listar_animais()
        lista_animais.delete("1.0", "end")
        for animal in animais:
            lista_animais.insert("end", f"ID: {animal[0]} - {animal[1]} ({animal[2]}) - Tutor: {animal[7]}\n")

    carregar_tutores()
    atualizar_lista()
    janela.mainloop()

if __name__ == "__main__":
    criar_tabela_animais()
    criar_janela_animais()