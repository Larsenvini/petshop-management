import customtkinter as ctk
from database.db_config import criar_conexao, executar_query, executar_select

def criar_tabela_servicos():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            duracao_minutos INTEGER,
            categoria TEXT
        )
    ''')
    conn.close()

def cadastrar_servico(nome, descricao, preco, duracao_minutos, categoria):
    executar_query('''
        INSERT INTO servicos (nome, descricao, preco, duracao_minutos, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, descricao, preco, duracao_minutos, categoria))

def listar_servicos():
    return executar_select('SELECT * FROM servicos')

def atualizar_servico(id_servico, nome, descricao, preco, duracao_minutos, categoria):
    executar_query('''
        UPDATE servicos 
        SET nome = ?, descricao = ?, preco = ?, duracao_minutos = ?, categoria = ?
        WHERE id = ?
    ''', (nome, descricao, preco, duracao_minutos, categoria, id_servico))

def excluir_servico(id_servico):
    executar_query('DELETE FROM servicos WHERE id = ?', (id_servico,))

def criar_janela_servicos():
    janela = ctk.CTk()
    janela.geometry("800x600")
    janela.title("Gerenciamento de Serviços")
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

    ctk.CTkLabel(frame_campos, text="Descrição:", font=label_font, text_color=text_color).grid(row=2, column=0, padx=10, pady=8, sticky="w")
    entrada_descricao = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_descricao.grid(row=2, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Preço:", font=label_font, text_color=text_color).grid(row=3, column=0, padx=10, pady=8, sticky="w")
    entrada_preco = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_preco.grid(row=3, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Duração (minutos):", font=label_font, text_color=text_color).grid(row=4, column=0, padx=10, pady=8, sticky="w")
    entrada_duracao = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_duracao.grid(row=4, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Categoria:", font=label_font, text_color=text_color).grid(row=5, column=0, padx=10, pady=8, sticky="w")
    lista_categoria = ctk.CTkComboBox(frame_campos, values=["Banho e Tosa", "Consulta Veterinária", "Vacinação", "Cirurgia", "Exames", "Hospedagem", "Adestramento", "Outros"], font=entry_font, width=250)
    lista_categoria.grid(row=5, column=1, padx=10, pady=8)
    lista_categoria.set("Banho e Tosa")

    frame_campos.grid_columnconfigure(0, weight=1)
    frame_campos.grid_columnconfigure(1, weight=3)
    
    def cadastrar():
        try:
            cadastrar_servico(
                entrada_nome.get(),
                "", # Descrição
                float(entrada_preco.get()),
                0, # Duração
                "" # Categoria
            )
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def atualizar():
        try:
            atualizar_servico(
                int(entrada_id.get()),
                entrada_nome.get(),
                "", # Descrição
                float(entrada_preco.get()),
                0, # Duração
                "" # Categoria
            )
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def excluir():
        try:
            excluir_servico(int(entrada_id.get()))
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def limpar_campos():
        entrada_id.delete(0, 'end')
        entrada_nome.delete(0, 'end')
        entrada_preco.delete(0, 'end')

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

    lista_servicos = ctk.CTkTextbox(frame_lista, fg_color="transparent", font=("Inter", 12), text_color="#333333")
    lista_servicos.pack(fill="both", expand=True, padx=10, pady=10)

    def atualizar_lista():
        servicos = listar_servicos()
        lista_servicos.delete("1.0", "end")
        for servico in servicos:
            lista_servicos.insert("end", f"ID: {servico[0]} - {servico[1]} - R${servico[3]:.2f} - {servico[4]}min - {servico[5]}\n")

    atualizar_lista()
    janela.mainloop()

if __name__ == "__main__":
    criar_tabela_servicos()
    criar_janela_servicos()