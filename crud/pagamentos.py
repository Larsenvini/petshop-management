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
    janela.geometry("800x600")
    janela.title("Gerenciamento de Pagamentos")
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

    ctk.CTkLabel(frame_campos, text="ID Agendamento:", font=label_font, text_color=text_color).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    entrada_agendamento_id = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_agendamento_id.grid(row=1, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Valor:", font=label_font, text_color=text_color).grid(row=2, column=0, padx=10, pady=8, sticky="w")
    entrada_valor = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_valor.grid(row=2, column=1, padx=10, pady=8)

    ctk.CTkLabel(frame_campos, text="Método de Pagamento:", font=label_font, text_color=text_color).grid(row=3, column=0, padx=10, pady=8, sticky="w")
    entrada_metodo = ctk.CTkEntry(frame_campos, font=entry_font, width=250)
    entrada_metodo.grid(row=3, column=1, padx=10, pady=8)

    frame_campos.grid_columnconfigure(0, weight=1)
    frame_campos.grid_columnconfigure(1, weight=3)
    
    def cadastrar():
        try:
            cadastrar_pagamento(entrada_agendamento_id.get(), entrada_valor.get(), entrada_metodo.get())
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def atualizar():
        try:
            # A função original 'atualizar_pagamento' espera status e data, 
            # que não estão no formulário. Usarei valores padrão.
            atualizar_pagamento(
                int(entrada_id.get()),
                float(entrada_valor.get()),
                entrada_metodo.get(),
                'pago', # Status padrão
                '' # Data padrão
            )
            limpar_campos()
            atualizar_lista()
        except (ValueError, IndexError):
            pass

    def excluir():
        try:
            excluir_pagamento(int(entrada_id.get()))
            limpar_campos()
            atualizar_lista()
        except ValueError:
            pass

    def limpar_campos():
        entrada_id.delete(0, 'end')
        entrada_agendamento_id.delete(0, 'end')
        entrada_valor.delete(0, 'end')
        entrada_metodo.delete(0, 'end')

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

    lista_pagamentos = ctk.CTkTextbox(frame_lista, fg_color="transparent", font=("Inter", 12), text_color="#333333")
    lista_pagamentos.pack(fill="both", expand=True, padx=10, pady=10)

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