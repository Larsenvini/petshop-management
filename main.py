import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from database.db_config import inicializar_banco
from crud.tutores import criar_janela_tutores
from crud.animais import criar_janela_animais
from crud.servicos import criar_janela_servicos
from crud.agendamentos import criar_janela_agendamentos
from crud.pagamentos import criar_janela_pagamentos

def focar_senha(event=None):
    entrada_senha.focus()

def realizar_login_event(event=None):
    verificar_login()

def login():
    def verificar_login():
        usuario = entrada_usuario.get()
        senha = entrada_senha.get()
        
        if usuario == "admin" and senha == "123":
            janela_login.destroy()
            menu_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    # Configuração da janela de login
    ctk.set_appearance_mode("light")
    janela_login = ctk.CTk()
    janela_login.geometry("500x500")
    try:
        janela_login.iconbitmap("assets/icon.ico")
    except:
        pass  # Ignora se o ícone não existir
    janela_login.title("Pet Shop - Login")
    janela_login.resizable(False, False)
    janela_login.configure(fg_color="#FFEADF")

    # Título principal
    loginText = ctk.CTkLabel(
        master=janela_login,
        text="Pet Shop",
        font=("Inter", 36, "bold"),
        text_color="#A25A31"
    )
    loginText.place(x=175, y=100)

    # Subtítulo
    subtitleText = ctk.CTkLabel(
        master=janela_login,
        text="Management System",
        font=("Inter", 14, "italic"),
        text_color="#A25A31"
    )
    subtitleText.place(x=185, y=140)

    # Ícones (com fallback caso não existam)
    try:
        user_pil = Image.open("assets/user.png")
        user_img = ctk.CTkImage(light_image=user_pil, size=(24, 24))
    except:
        user_img = None

    try:
        password_pil = Image.open("assets/password.png")
        password_img = ctk.CTkImage(light_image=password_pil, size=(24, 24))
    except:
        password_img = None

    # Frame do campo usuário
    entradaUsuario_frame = ctk.CTkFrame(
        master=janela_login,
        fg_color="#D9D9D9",
        corner_radius=50,
        width=234,
        height=41
    )
    entradaUsuario_frame.place(x=133, y=200)

    # Ícone do usuário (se disponível)
    if user_img:
        user_icon_label = ctk.CTkLabel(entradaUsuario_frame, image=user_img, text="")
        user_icon_label.place(x=10, y=8)
        entry_x = 35
    else:
        entry_x = 15

    # Campo de entrada do usuário
    entrada_usuario = ctk.CTkEntry(
        entradaUsuario_frame,
        placeholder_text="Usuário",
        font=("Inter", 12, "italic"),
        text_color="#A25A31",
        fg_color="#D9D9D9",
        placeholder_text_color="#A25A31",
        border_width=0,
        width=180 if user_img else 200
    )
    entrada_usuario.place(x=entry_x, y=8)
    entrada_usuario.bind("<Return>", focar_senha)

    # Frame do campo senha
    entradaSenha_frame = ctk.CTkFrame(
        master=janela_login,
        fg_color="#D9D9D9",
        corner_radius=50,
        width=234,
        height=41
    )
    entradaSenha_frame.place(x=133, y=254)

    # Ícone da senha (se disponível)
    if password_img:
        password_icon_label = ctk.CTkLabel(entradaSenha_frame, image=password_img, text="")
        password_icon_label.place(x=10, y=8)

    # Campo de entrada da senha
    entrada_senha = ctk.CTkEntry(
        entradaSenha_frame,
        placeholder_text="Senha",
        font=("Inter", 12, "italic"),
        text_color="#A25A31",
        fg_color="#D9D9D9",
        placeholder_text_color="#A25A31",
        border_width=0,
        width=180 if password_img else 200,
        show="*"
    )
    entrada_senha.place(x=entry_x, y=8)
    entrada_senha.bind("<Return>", realizar_login_event)

    # Botão de entrar
    entrarButton = ctk.CTkButton(
        master=janela_login,
        text="Entrar",
        font=("Inter", 16, "bold"),
        text_color="#EBBFA7",
        fg_color="#A25A31",
        hover_color="#663A20",
        width=234,
        height=41,
        corner_radius=50,
        command=verificar_login
    )
    entrarButton.place(x=133, y=307)

    janela_login.mainloop()

def menu_principal():
    janela = ctk.CTk()
    janela.geometry("700x600")
    janela.title("Pet Shop - Menu Principal")
    try:
        janela.iconbitmap("assets/icon.ico")
    except:
        pass
    janela.resizable(False, False)
    janela.configure(fg_color="#FFEADF")

    # Título principal
    titleText = ctk.CTkLabel(
        master=janela,
        text="Pet Shop",
        font=("Inter", 42, "bold"),
        text_color="#A25A31"
    )
    titleText.place(x=250, y=50)

    # Subtítulo
    subtitleText = ctk.CTkLabel(
        master=janela,
        text="Sistema de Gestão",
        font=("Inter", 18, "italic"),
        text_color="#A25A31"
    )
    subtitleText.place(x=275, y=100)

    # Frame principal dos botões
    frame_botoes = ctk.CTkFrame(
        master=janela,
        fg_color="#D9D9D9",
        corner_radius=20,
        width=500,
        height=400
    )
    frame_botoes.place(x=100, y=150)

    # Estilo consistente para todos os botões
    button_style = {
        "font": ("Inter", 16, "bold"),
        "text_color": "#EBBFA7",
        "fg_color": "#A25A31",
        "hover_color": "#663A20",
        "width": 400,
        "height": 45,
        "corner_radius": 25
    }

    # Botões do menu
    ctk.CTkButton(
        master=frame_botoes,
        text="👥 Gerenciar Tutores",
        command=criar_janela_tutores,
        **button_style
    ).place(x=50, y=30)

    ctk.CTkButton(
        master=frame_botoes,
        text="🐕 Gerenciar Animais",
        command=criar_janela_animais,
        **button_style
    ).place(x=50, y=90)

    ctk.CTkButton(
        master=frame_botoes,
        text="🛠️ Gerenciar Serviços",
        command=criar_janela_servicos,
        **button_style
    ).place(x=50, y=150)

    ctk.CTkButton(
        master=frame_botoes,
        text="📅 Gerenciar Agendamentos",
        command=criar_janela_agendamentos,
        **button_style
    ).place(x=50, y=210)

    ctk.CTkButton(
        master=frame_botoes,
        text="💰 Gerenciar Pagamentos",
        command=criar_janela_pagamentos,
        **button_style
    ).place(x=50, y=270)

    # Botão sair com estilo diferenciado
    sair_button = ctk.CTkButton(
        master=frame_botoes,
        text="❌ Sair",
        command=janela.quit,
        font=("Inter", 16, "bold"),
        text_color="#FFFFFF",
        fg_color="#CC4125",
        hover_color="#A63419",
        width=400,
        height=45,
        corner_radius=25
    )
    sair_button.place(x=50, y=330)

    janela.mainloop()

if __name__ == "__main__":
    inicializar_banco()
    login()