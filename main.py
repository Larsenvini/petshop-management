import customtkinter as ctk
from tkinter import *
from PIL import Image
from tkinter import messagebox
import sqlite3

def sair():
    global telaPrincipal
    telaPrincipal.destroy()

def listar_tutores():

    ctk.set_appearance_mode("light")


    listar = ctk.CTk()
    listar.geometry("700x540")
    listar.title("Lista de Tutores")
    listar.configure(fg_color="#FFEADF")
    listar.resizable(False, False)
    listar.iconbitmap("assets/icon.ico")

    titulo = ctk.CTkLabel(listar, text="Informações", font=("Inter", 16, "bold"), text_color="#683B21")
    titulo.place(x=30, y=20)

    pesquisaEntry = ctk.CTkEntry(
        listar,
        width=250,
        placeholder_text="Pesquisar por nome",
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        placeholder_text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30
    )
    pesquisaEntry.place(x=30, y=60)

    tutores = []

    def carregar_tutores():
        conn = sqlite3.connect('database/tutores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tutores")
        resultado = cursor.fetchall()
        conn.close()
        return resultado

    def atualizar_listbox():
        listbox.delete(0, END)
        nonlocal tutores
        tutores = carregar_tutores()
        for tutor in tutores:
            listbox.insert(END, tutor[1])  

    def filtrar_lista():
        termo = pesquisaEntry.get().lower()
        listbox.delete(0, END)
        for tutor in tutores:
            if termo in tutor[1].lower():
                listbox.insert(END, tutor[1])

    botaoPesquisar = ctk.CTkButton(
        listar,
        text="Pesquisar",
        text_color="#FFFFFF",
        command=filtrar_lista,
        width=90,
        fg_color="#663A20",
        hover_color="#502D19",
        font=("Inter", 12, "bold"),
        corner_radius=30
    )
    botaoPesquisar.place(x=290, y=60)

    scrollbar = Scrollbar(listar)
    scrollbar.place(x=265, y=100, height=280)

    listbox = Listbox(
        listar,
        width=33,
        height=17,
        font=("Inter", 10, "bold"),
        fg="#663A20",
        bg="#D1D1D1",
        yscrollcommand=scrollbar.set,
        borderwidth=0,
        highlightthickness=1
    )
    listbox.place(x=30, y=100)
    scrollbar.config(command=listbox.yview)

    atualizar_listbox()

    campos = {}
    labels = [
        ("Nome", "nome"),
        ("CPF", "cpf"),
        ("Email", "email"),
        ("Telefone", "telefone"),
        ("Endereço", "endereco"),
        ("Bairro", "bairro"),
        ("Cidade", "cidade"),
        ("Estado", "estado")
    ]

    y = 100
    for label_text, key in labels:
        lbl = ctk.CTkLabel(listar, text=f"{label_text}:", font=("Inter", 12, "bold"), text_color="#683B21")
        lbl.place(x=300, y=y)

        entry = ctk.CTkEntry(
            listar,
            width=250,
            height=27,
            font=("Inter", 12, "bold"),
            text_color="#683B21",
            fg_color="#D9D9D9",
            corner_radius=30,
            border_width=0
        )
        entry.place(x=380, y=y)
        entry.configure(state="readonly")
        campos[key] = entry

        y += 40

    id_selecionado = {"id": None}

    def mostrar_detalhes(event):
        selecao = listbox.curselection()
        if selecao:
            index = selecao[0]
            tutor = tutores[index]
            id_selecionado["id"] = tutor[0]

            valores = {
                "nome": tutor[1], "cpf": tutor[2], "email": tutor[3], "telefone": tutor[4],
                "endereco": tutor[5], "bairro": tutor[6], "cidade": tutor[7], "estado": tutor[8]
            }

            for key, value in valores.items():
                campos[key].configure(state="normal")
                campos[key].delete(0, END)
                campos[key].insert(0, value if value else "")
                campos[key].configure(state="readonly")

    listbox.bind("<<ListboxSelect>>", mostrar_detalhes)

    def liberar_edicao():
        if id_selecionado["id"] is None:
            messagebox.showwarning("Nenhum selecionado", "Selecione um tutor para editar.")
            return
        for campo in campos.values():
            campo.configure(state="normal")

    def atualizar_tutor():
        id_tutor = id_selecionado["id"]
        if id_tutor is None:
            messagebox.showwarning("Seleção necessária", "Selecione um tutor na lista para atualizar.")
            return

        dados = {key: campos[key].get() for key in campos}
        if not dados["nome"] or not dados["cpf"]:
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios.")
            return

        try:
            conn = sqlite3.connect("database/tutores.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tutores SET 
                    nome = ?, cpf = ?, email = ?, telefone = ?, 
                    endereco = ?, bairro = ?, cidade = ?, estado = ?
                WHERE id = ?
            """, (
                dados["nome"], dados["cpf"], dados["email"], dados["telefone"],
                dados["endereco"], dados["bairro"], dados["cidade"], dados["estado"],
                id_tutor
            ))
            conn.commit()
            conn.close()

            atualizar_listbox()
            messagebox.showinfo("Sucesso", "Informações atualizadas com sucesso!")

            for campo in campos.values():
                campo.configure(state="readonly")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar tutor:\n{e}")

    def excluir_tutor():
        id_tutor = id_selecionado["id"]
        if id_tutor is not None:
            resposta = messagebox.askyesno("Excluir", "Tem certeza que deseja excluir este tutor?")
            if resposta:
                conn = sqlite3.connect('database/tutores.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tutores WHERE id = ?", (id_tutor,))
                conn.commit()
                conn.close()
                atualizar_listbox()
                for campo in campos.values():
                    campo.configure(state="normal")
                    campo.delete(0, END)
                    campo.configure(state="readonly")
                id_selecionado["id"] = None
                messagebox.showinfo("Sucesso", "Tutor excluído com sucesso.")

    editarBtn = ctk.CTkButton(
        listar,
        text="Editar",
        font=("Inter", 12, "bold"),
        text_color="#FFFFFF",
        fg_color="#683B21",
        hover_color="#522D18",
        corner_radius=30,
        width=90,
        command=liberar_edicao
    )
    editarBtn.place(x=387, y=60)

    atualizarBtn = ctk.CTkButton(
        listar,
        text="Atualizar",
        font=("Inter", 12, "bold"),
        text_color="#FFFFFF",
        fg_color="#683B21",
        hover_color="#522D18",
        corner_radius=30,
        width=100,
        command=atualizar_tutor
    )
    atualizarBtn.place(x=484, y=60)

    excluirBtn = ctk.CTkButton(
        listar,
        text="Excluir",
        font=("Inter", 12, "bold"),
        text_color="#FFFFFF",
        fg_color="#683B21",
        hover_color="#522D18",
        corner_radius=30,
        width=236.5,
        command=excluir_tutor
    )
    excluirBtn.place(x=30, y=400)

    voltarBtn = ctk.CTkButton(
        listar,
        text="Voltar",
        font=("Inter", 12, "bold"),
        text_color="#FFFFFF",
        fg_color="#80411E",
        hover_color="#582C15",
        corner_radius=30,
        width=70,
        command=lambda: [listar.destroy(), menu_tutor()]
    )
    voltarBtn.place(x=585, y=460)

    listar.mainloop()

def criar_tabela_tutores():
    conn = sqlite3.connect('database/tutores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            endereco TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT
        )
    ''')
    conn.commit()
    conn.close()

def abrir_menu_tutor():
    telaPrincipal.destroy()
    menu_tutor()

def cadastro_tutor():

    def on_salvar():
        nome = nomeTutorEntry.get()
        cpf = cpfTutorEntry.get()
        email = emailTutorEntry.get()
        telefone = telefoneTutorEntry.get()
        endereco = enderecoTutorEntry.get()
        bairro = bairroTutorEntry.get()
        cidade = cidadeTutorEntry.get()
        estado = estadoTutorEntry.get()

        if not nome or not cpf:
            messagebox.showwarning("Atenção", "Nome e CPF são obrigatórios.")
            return

        conn = sqlite3.connect('database/tutores.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO tutores (nome, cpf, email, telefone, endereco, bairro, cidade, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, cpf, email, telefone, endereco, bairro, cidade, estado))
        conn.commit()
        conn.close()
    
        messagebox.showinfo("Sucesso", "Tutor cadastrado com sucesso!")
        cadastroTutor.destroy()  # Fecha a janela de cadastro

    ctk.set_appearance_mode("light")

    cadastroTutor = ctk.CTk()
    cadastroTutor.geometry("550x500")
    cadastroTutor.iconbitmap("assets/icon.ico")
    cadastroTutor.title("Cadastro - Tutor")
    cadastroTutor.resizable(False, False)
    cadastroTutor.configure(fg_color="#FFEADF")

    cadastrarInformacoesText = ctk.CTkLabel(
        master=cadastroTutor,
        text="Cadastrar Informações",
        font=("Inter", 16, "bold"),
        text_color="#683B21"
    )
    cadastrarInformacoesText.place(x=28, y=45)

    nomeTutor = ctk.CTkLabel(
        master=cadastroTutor,
        text="Nome Completo",
        font=("Inter", 12, "bold"),
        text_color="#683B21"
    )
    nomeTutor.place(x=28, y=85)

    nomeTutorEntry = ctk.CTkEntry(
        master=cadastroTutor,
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30,
        width=225,
        height=27
    )
    nomeTutorEntry.place(x=28, y=110)

    cpfTutor = ctk.CTkLabel(
        master=cadastroTutor,
        text="CPF",
        font=("Inter", 12, "bold"),
        text_color="#683B21"
    )
    cpfTutor.place(x=28, y=150)

    cpfTutorEntry = ctk.CTkEntry(
        master=cadastroTutor,
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30,
        width=225,
        height=27
    )
    cpfTutorEntry.place(x=28, y=175)
    nomeTutorEntry.bind("<Return>", lambda e: cpfTutorEntry.focus_set())

    emailTutor = ctk.CTkLabel(
        master=cadastroTutor,
        text="Email",
        font=("Inter", 12, "bold"),
        text_color="#683B21"
    )
    emailTutor.place(x=28, y=215)

    emailTutorEntry = ctk.CTkEntry(
        master=cadastroTutor,
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30,
        width=225,
        height=27
    )
    emailTutorEntry.place(x=28, y=240)
    cpfTutorEntry.bind("<Return>", lambda e: emailTutorEntry.focus_set())

    telefoneTutor = ctk.CTkLabel(
        master=cadastroTutor,
        text="Telefone",
        font=("Inter", 12, "bold"),
        text_color="#683B21"
    )
    telefoneTutor.place(x=28, y=280)

    telefoneTutorEntry = ctk.CTkEntry(
        master=cadastroTutor,
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30,
        width=225,
        height=27
    )
    telefoneTutorEntry.place(x=28, y=305)
    emailTutorEntry.bind("<Return>", lambda e: telefoneTutorEntry.focus_set())

    enderecoTutor = ctk.CTkLabel(
        master=cadastroTutor,
        text="Endereço",
        font=("Inter", 12, "bold"),
        text_color="#683B21"
    )
    enderecoTutor.place(x=275, y=85)

    enderecoTutorEntry = ctk.CTkEntry(
        master=cadastroTutor,
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30,
        width=225,
        height=27
    )
    enderecoTutorEntry.place(x=275, y=110)
    telefoneTutorEntry.bind("<Return>", lambda e: enderecoTutorEntry.focus_set())

    bairroTutor = ctk.CTkLabel(
        master=cadastroTutor,
        text="Bairro",
        font=("Inter", 12, "bold"),
        text_color="#683B21"
    )
    bairroTutor.place(x=275, y=150)

    bairroTutorEntry = ctk.CTkEntry(
        master=cadastroTutor,
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30,
        width=225,
        height=27
    )
    bairroTutorEntry.place(x=275, y=175)
    enderecoTutorEntry.bind("<Return>", lambda e: bairroTutorEntry.focus_set())

    cidadeTutor = ctk.CTkLabel(
        master=cadastroTutor,
        text="Cidade",
        font=("Inter", 12, "bold"),
        text_color="#683B21"
    )
    cidadeTutor.place(x=275, y=215)

    cidadeTutorEntry = ctk.CTkEntry(
        master=cadastroTutor,
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30,
        width=225,
        height=27
    )
    cidadeTutorEntry.place(x=275, y=240)
    bairroTutorEntry.bind("<Return>", lambda e: cidadeTutorEntry.focus_set())

    estadoTutor = ctk.CTkLabel(
        master=cadastroTutor,
        text="Estado",
        font=("Inter", 12, "bold"),
        text_color="#683B21"
    )
    estadoTutor.place(x=275, y=280)

    estadoTutorEntry = ctk.CTkEntry(
        master=cadastroTutor,
        font=("Inter", 12, "bold"),
        text_color="#683B21",
        fg_color="#C2C2C2",
        border_width=0,
        corner_radius=30,
        width=225,
        height=27
    )
    estadoTutorEntry.place(x=275, y=305)
    cidadeTutorEntry.bind("<Return>", lambda e: estadoTutorEntry.focus_set())

    salvarButton = ctk.CTkButton(
        master=cadastroTutor,
        text="Salvar",
        font=("Inter", 14, "bold"),
        text_color="#FFFFFF",
        fg_color="#683B21",
        hover_color="#4A2815",
        corner_radius=30,
        width=100,
        height=35
    )
    salvarButton.place(x=400, y=400)
    salvarButton.configure(command=on_salvar)
    estadoTutorEntry.bind("<Return>", lambda e: salvarButton.focus_set())

    cadastrarPetButton = ctk.CTkButton(
        master=cadastroTutor,
        text="Associar Pet",
        font=("Inter", 14, "bold"),
        text_color="#DB9972",
        fg_color="#613924",
        hover_color="#492917",
        corner_radius=30,
        width=100,
        height=35,
        cursor="hand2"
        )
    cadastrarPetButton.place(x=270, y=400)

    cadastroTutor.mainloop()
  
def abrir_menu():
    ctk.set_appearance_mode("light")

    global telaPrincipal
    telaPrincipal = ctk.CTk()
    telaPrincipal.geometry("550x500")
    telaPrincipal.iconbitmap("assets/icon.ico")
    telaPrincipal.title("Tela Principal")
    telaPrincipal.resizable(False, False)
    telaPrincipal.configure(fg_color="#FFEADF")

    image_pil = Image.open("assets/image.png")
    image = ctk.CTkImage(light_image=image_pil, size=(270, 500))
    telaPrincipal.image_ref = image

    image_label = ctk.CTkLabel(
        master=telaPrincipal,
        text="", 
        image=image,
        width=279,
        height=500
    )
    image_label.place(x=280, y=0)

    bemVindoText = ctk.CTkLabel(
        master=telaPrincipal,
        text="Seja-bem vindo ao",
        font=("Inter", 16, "bold"),
        text_color="#A25A31"
    )
    bemVindoText.place(x=54, y=112)

    menuPrincipalText = ctk.CTkLabel(
        master=telaPrincipal,
        text="Menu Principal",
        font=("Inter", 16, "italic"),
        text_color="#4D2C19"
    )
    menuPrincipalText.place(x=69, y=131)

    tutorButton = ctk.CTkButton(
        master=telaPrincipal,
        text="Tutores",
        text_color="#EBBFA7",
        font=("Inter", 14, "bold"),
        fg_color="#A25A31",
        hover_color="#663A20",
        width=143,
        height=30,
        command=abrir_menu_tutor
    )
    tutorButton.place(x=55, y=179)

    petButton = ctk.CTkButton(
        master=telaPrincipal,
        text="Pets",
        text_color="#EBBFA7",
        font=("Inter", 14, "bold"),
        fg_color="#A25A31",
        hover_color="#663A20",
        width=143,
        height=30
    )
    petButton.place(x=55, y=221)

    servicosButton = ctk.CTkButton(
        master=telaPrincipal,
        text="Serviços",
        text_color="#EBBFA7",
        font=("Inter", 14, "bold"),
        fg_color="#A25A31",
        hover_color="#663A20",
        width=143,
        height=30,
        cursor = "hand2"
    )
    servicosButton.place(x=55, y=263)

    agendamentosButton = ctk.CTkButton(
        master=telaPrincipal,
        text="Agendamentos",
        text_color="#EBBFA7",
        font=("Inter", 14, "bold"),
        fg_color="#A25A31",
        hover_color="#663A20",
        width=143,
        height=30,
        cursor="hand2"
    )
    agendamentosButton.place(x=55, y=305)

    pagamentosButton = ctk.CTkButton(
        master=telaPrincipal,
        text="Pagamentos",
        text_color="#EBBFA7",
        font=("Inter", 14, "bold"),
        fg_color="#A25A31",
        hover_color="#663A20",
        width=143,
        height=30,
        cursor="hand2"
    )
    pagamentosButton.place(x=55, y=347)

    sairButton = ctk.CTkLabel(
        master=telaPrincipal,
        text="Sair",
        text_color="#663A20",
        font=("Inter", 10, "bold"),
        fg_color="transparent",
        cursor="hand2"
    )
    sairButton.place(x=120, y=446)
    sairButton.bind("<Button-1>", lambda e: sair())

    telaPrincipal.mainloop()

def menu_tutor():
    ctk.set_appearance_mode("light")

    menuTutor = ctk.CTk()
    menuTutor.geometry("550x500")
    menuTutor.iconbitmap("assets/icon.ico")
    menuTutor.title("Menu de Tutores")
    menuTutor.resizable(False, False)
    menuTutor.configure(fg_color="#FFEADF")

    image2_pil = Image.open("assets/image2.png")
    image2 = ctk.CTkImage(light_image=image2_pil, size=(270, 500))
    menuTutor.image2_ref = image2

    image2_label = ctk.CTkLabel(
        master=menuTutor,
        text="",
        image=image2,
        width=279,
        height=500
    )
    image2_label.place(x=280, y=0)

    tutoresText = ctk.CTkLabel(
        master=menuTutor,
        text="Tutores",
        font=("Inter", 20, "bold"),
        text_color="#A25A31"
    )
    tutoresText.place(x=91, y=101)

    cadastrarButton = ctk.CTkButton(
        master=menuTutor,
        text="Cadastro",
        text_color="#FFEADF",
        font=("Inter", 13, "bold"),
        fg_color="#A25A31",
        hover_color="#663A20",
        corner_radius=10,
        width=145,
        height=35,
        cursor="hand2",
        command=cadastro_tutor
    )
    cadastrarButton.place(x=59, y=134)

    editarButton = ctk.CTkButton(
        master=menuTutor,
        text="Listar Informações",
        text_color="#FFEADF",
        font=("Inter", 13, "bold"),
        fg_color="#A25A31",
        hover_color="#663A20",
        corner_radius=10,
        width=145,
        height=35,
        cursor="hand2",
        command= listar_tutores
    )
    editarButton.place(x=59, y=179)

    voltarButton = ctk.CTkButton(
        master=menuTutor,
        text="Voltar",
        text_color="#FFEADF",
        font=("Inter", 13, "bold"),
        fg_color="#663A20",
        hover_color="#472A18",
        corner_radius=10,
        width=145,
        height=35,
        command=lambda: [menuTutor.destroy(), abrir_menu()]
    )
    voltarButton.place(x=59, y=224)

    menuTutor.mainloop()

criar_tabela_tutores()

