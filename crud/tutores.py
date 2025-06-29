import customtkinter as ctk
from database.db_config import criar_conexao, executar_query, executar_select

def criar_tabela_tutores():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT,
            endereco TEXT,
            cpf TEXT UNIQUE
        )
    ''')
    conn.close()

def cadastrar_tutor(nome, telefone, email, endereco, cpf):
    executar_query('''
        INSERT INTO tutores (nome, telefone, email, endereco, cpf)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, telefone, email, endereco, cpf))

def listar_tutores():
    return executar_select('SELECT * FROM tutores')

def atualizar_tutor(id_tutor, nome, telefone, email, endereco, cpf):
    executar_query('''
        UPDATE tutores 
        SET nome = ?, telefone = ?, email = ?, endereco = ?, cpf = ?
        WHERE id = ?
    ''', (nome, telefone, email, endereco, cpf, id_tutor))

def excluir_tutor(id_tutor):
    executar_query('DELETE FROM tutores WHERE id = ?', (id_tutor,))

def criar_janela_tutores():
    janela = ctk.CTk()
    janela.geometry("800x600")
    janela.title("Gerenciamento de Tutores")
    janela.configure(fg_color="#FFFFFF")

    frame_campos = ctk.CTkFrame(janela, fg_color="#FFFFFF")
    frame_campos.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(frame_campos, text="ID (para editar/excluir):").grid(row=0, column=0, padx=5, pady=5)
    entrada_id = ctk.CTkEntry(frame_campos)
    entrada_id.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
    entrada_nome = ctk.CTkEntry(frame_campos)
    entrada_nome.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Telefone:").grid(row=2, column=0, padx=5, pady=5)
    entrada_telefone = ctk.CTkEntry(frame_campos)
    entrada_telefone.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Email:").grid(row=3, column=0, padx=5, pady=5)
    entrada_email = ctk.CTkEntry(frame_campos)
    entrada_email.grid(row=3, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="Endereço:").grid(row=4, column=0, padx=5, pady=5)
    entrada_endereco = ctk.CTkEntry(frame_campos)
    entrada_endereco.grid(row=4, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame_campos, text="CPF:").grid(row=5, column=0, padx=5, pady=5)
    entrada_cpf = ctk.CTkEntry(frame_campos)
    entrada_cpf.grid(row=5, column=1, padx=5, pady=5)

    def cadastrar():
        try:
            cadastrar_tutor(
                entrada_nome.get(),
                entrada_telefone.get(),
                entrada_email.get(),
                entrada_endereco.get(),
                entrada_cpf.get()
            )
            limpar_campos()
            atualizar_lista()
        except Exception:
            pass

    def atualizar():
        try:
            atualizar_tutor(
                int(entrada_id.get()),
                entrada_nome.get(),
                entrada_telefone.get(),
                entrada_email.get(),
                entrada_endereco.get(),
                entrada_cpf.get()
            )
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def excluir():
        try:
            excluir_tutor(int(entrada_id.get()))
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def limpar_campos():
        entrada_id.delete(0, 'end')
        entrada_nome.delete(0, 'end')
        entrada_telefone.delete(0, 'end')
        entrada_email.delete(0, 'end')
        entrada_endereco.delete(0, 'end')
        entrada_cpf.delete(0, 'end')

    frame_botoes = ctk.CTkFrame(janela, fg_color="#2196F3")
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Atualizar", command=atualizar).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Excluir", command=excluir).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes, text="Limpar", command=limpar_campos).pack(side="left", padx=5)

    frame_lista = ctk.CTkFrame(janela, fg_color="#2196F3")
    frame_lista.pack(fill="both", expand=True, padx=20, pady=20)

    lista_tutores = ctk.CTkTextbox(frame_lista)
    lista_tutores.pack(fill="both", expand=True)

    def atualizar_lista():
        tutores = listar_tutores()
        lista_tutores.delete("1.0", "end")
        for tutor in tutores:
            lista_tutores.insert("end", f"ID: {tutor[0]} - {tutor[1]} - Tel: {tutor[2]} - Email: {tutor[3]}\n")

    atualizar_lista()
    janela.mainloop()

if __name__ == "__main__":
    criar_tabela_tutores()
    criar_janela_tutores()