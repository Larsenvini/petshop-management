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
    janela.configure(fg_color="#FFFFFF")

    frame_campos = ctk.CTkFrame(janela, fg_color="#FFFFFF")
    frame_campos.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(frame_campos, text="ID (para editar/excluir):").grid(row=0, column=0, padx=5, pady=5)
    entrada_id = ctk.CTkEntry(frame_campos)
    entrada_id.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
    entrada_nome = ctk.CTkEntry(frame_campos)
    entrada_nome.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Descrição:").grid(row=2, column=0, padx=5, pady=5)
    entrada_descricao = ctk.CTkEntry(frame_campos)
    entrada_descricao.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Preço:").grid(row=3, column=0, padx=5, pady=5)
    entrada_preco = ctk.CTkEntry(frame_campos)
    entrada_preco.grid(row=3, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Duração (minutos):").grid(row=4, column=0, padx=5, pady=5)
    entrada_duracao = ctk.CTkEntry(frame_campos)
    entrada_duracao.grid(row=4, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Categoria:").grid(row=5, column=0, padx=5, pady=5)
    lista_categoria = ctk.CTkComboBox(frame_campos, values=["Banho e Tosa", "Consulta Veterinária", "Vacinação", "Cirurgia", "Exames", "Hospedagem", "Adestramento", "Outros"])
    lista_categoria.grid(row=5, column=1, padx=5, pady=5)
    lista_categoria.set("Banho e Tosa")

    def cadastrar():
        try:
            cadastrar_servico(
                entrada_nome.get(),
                entrada_descricao.get(),
                float(entrada_preco.get()),
                int(entrada_duracao.get()),
                lista_categoria.get()
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
                entrada_descricao.get(),
                float(entrada_preco.get()),
                int(entrada_duracao.get()),
                lista_categoria.get()
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
        entrada_descricao.delete(0, 'end')
        entrada_preco.delete(0, 'end')
        entrada_duracao.delete(0, 'end')

    frame_botoes = ctk.CTkFrame(janela, fg_color="#2196F3")
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Atualizar", command=atualizar).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Excluir", command=excluir).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Limpar", command=limpar_campos).pack(side="left", padx=5)

    frame_lista = ctk.CTkFrame(janela, fg_color="#2196F3")
    frame_lista.pack(fill="both", expand=True, padx=20, pady=20)

    lista_servicos = ctk.CTkTextbox(frame_lista)
    lista_servicos.pack(fill="both", expand=True)

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