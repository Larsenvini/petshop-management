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
            preco_base REAL NOT NULL,
            duracao INTEGER NOT NULL,
            status TEXT DEFAULT 'ativo'
        )
    ''')
    conn.close()

def cadastrar_servico(nome, descricao, preco_base, duracao):
    executar_query('''
        INSERT INTO servicos (nome, descricao, preco_base, duracao)
        VALUES (?, ?, ?, ?)
    ''', (nome, descricao, preco_base, duracao))

def listar_servicos():
    return executar_select('SELECT * FROM servicos')

def atualizar_servico(id_servico, nome, descricao, preco_base, duracao):
    executar_query('''
        UPDATE servicos 
        SET nome = ?, descricao = ?, preco_base = ?, duracao = ?
        WHERE id = ?
    ''', (nome, descricao, preco_base, duracao, id_servico))

def excluir_servico(id_servico):
    executar_query('DELETE FROM servicos WHERE id = ?', (id_servico,))

def criar_janela_servicos():
    janela = ctk.CTk()
    janela.geometry("800x600")
    janela.title("Gerenciamento de Serviços")
    janela.configure(fg_color="#FFEADF")

    # Campos de entrada
    frame_campos = ctk.CTkFrame(janela, fg_color="#D9D9D9")
    frame_campos.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(frame_campos, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entrada_nome = ctk.CTkEntry(frame_campos)
    entrada_nome.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
    entrada_descricao = ctk.CTkEntry(frame_campos)
    entrada_descricao.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Preço Base:").grid(row=2, column=0, padx=5, pady=5)
    entrada_preco = ctk.CTkEntry(frame_campos)
    entrada_preco.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Duração (min):").grid(row=3, column=0, padx=5, pady=5)
    entrada_duracao = ctk.CTkEntry(frame_campos)
    entrada_duracao.grid(row=3, column=1, padx=5, pady=5)

    # Botões
    frame_botoes = ctk.CTkFrame(janela, fg_color="#D9D9D9")
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=lambda: cadastrar_servico(
        entrada_nome.get(),
        entrada_descricao.get(),
        entrada_preco.get(),
        entrada_duracao.get()
    )).pack(side="left", padx=5)

    ctk.CTkButton(frame_botoes, text="Atualizar", command=lambda: atualizar_servico(
        entrada_id.get(),
        entrada_nome.get(),
        entrada_descricao.get(),
        entrada_preco.get(),
        entrada_duracao.get()
    )).pack(side="left", padx=5)

    ctk.CTkButton(frame_botoes, text="Excluir", command=lambda: excluir_servico(entrada_id.get())).pack(side="left", padx=5)

    # Lista de serviços
    frame_lista = ctk.CTkFrame(janela, fg_color="#D9D9D9")
    frame_lista.pack(fill="both", expand=True, padx=20, pady=20)

    lista_servicos = ctk.CTkTextbox(frame_lista)
    lista_servicos.pack(fill="both", expand=True)

    # Função para atualizar lista
    def atualizar_lista():
        servicos = listar_servicos()
        lista_servicos.delete("1.0", "end")
        for servico in servicos:
            lista_servicos.insert("end", f"ID: {servico[0]} - {servico[1]} - R${servico[3]:.2f} - {servico[4]}min\n")

    atualizar_lista()

    janela.mainloop()

if __name__ == "__main__":
    criar_tabela_servicos()
    criar_janela_servicos()
