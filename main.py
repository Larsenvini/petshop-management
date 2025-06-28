import customtkinter as ctk
from tkinter import messagebox
from tkinter import *
from PIL import Image
from crud.tutores import criar_janela_tutores
from crud.animais import criar_janela_animais
from crud.agendamentos import criar_janela_agendamentos
from crud.pagamentos import criar_janela_pagamentos
from crud.servicos import criar_janela_servicos
import sys
import os

def mostrar_login():
    janela_login = ctk.CTk()
    janela_login.geometry("500x500")
    janela_login.iconbitmap("assets/icon.ico")
    janela_login.title("Painel de Login")
    janela_login.resizable(False, False)
    janela_login.configure(fg_color="#FFEADF")

    def focar_senha(event=None):
        entradaSenha.focus()

    def realizar_login_event(event=None):
        realizar_login()

    def realizar_login():
        usuario = entradaUsuario.get()
        padrao_usuario = usuario.lower()
        usuario_senha = padrao_usuario + "123"
        senha = entradaSenha.get()

        if senha == usuario_senha:
            janela_login.destroy()
            abrir_menu()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def pular_login():
        janela_login.destroy()
        abrir_menu()

    ctk.set_appearance_mode("light")

    # Interface do login
    loginText = ctk.CTkLabel(
        master=janela_login,
        text="Login",
        font=("Inter", 36, "bold"),
        text_color="#A25A31"
    )
    loginText.place(x=201, y=128)

    # Campo de usuário
    user_pil = Image.open("assets/user.png")
    user_img = ctk.CTkImage(light_image=user_pil, size=(24, 24))

    entradaUsuario_frame = ctk.CTkFrame(
        master=janela_login,
        fg_color="#D9D9D9",
        corner_radius=50,
        width=234,
        height=41
    )
    entradaUsuario_frame.place(x=133, y=183)

    user_icon_label = ctk.CTkLabel(entradaUsuario_frame, image=user_img, text="")
    user_icon_label.place(x=10, y=8)

    entradaUsuario = ctk.CTkEntry(
        entradaUsuario_frame,
        placeholder_text="Usuário",
        font=("Inter", 12, "italic"),
        text_color="#A25A31",
        fg_color="#D9D9D9",
        placeholder_text_color="#A25A31",
        border_width=0,
        width=180
    )
    entradaUsuario.place(x=35, y=8)
    entradaUsuario.bind("<Return>", focar_senha)

    # Campo de senha
    password_pil = Image.open("assets/password.png")
    password_img = ctk.CTkImage(light_image=password_pil, size=(24, 24))

    entradaSenha_frame = ctk.CTkFrame(
        master=janela_login,
        fg_color="#D9D9D9",
        corner_radius=50,
        width=234,
        height=41
    )
    entradaSenha_frame.place(x=133, y=237)

    password_icon_label = ctk.CTkLabel(entradaSenha_frame, image=password_img, text="")
    password_icon_label.place(x=10, y=8)

    entradaSenha = ctk.CTkEntry(
        entradaSenha_frame,
        placeholder_text="Senha",
        font=("Inter", 12, "italic"),
        text_color="#A25A31",
        fg_color="#D9D9D9",
        placeholder_text_color="#A25A31",
        border_width=0,
        width=180,
        show="*"
    )
    entradaSenha.place(x=35, y=8)
    entradaSenha.bind("<Return>", realizar_login_event)

    # Botões
    frame_botoes = ctk.CTkFrame(janela_login, fg_color="transparent")
    frame_botoes.pack(pady=20)

    # Botão Entrar
    entrarButton = ctk.CTkButton(
        master=frame_botoes,
        text="Entrar",
        font=("Inter", 16, "bold"),
        text_color="#EBBFA7",
        fg_color="#A25A31",
        hover_color="#663A20",
        width=200,
        height=40,
        command=realizar_login
    )
    entrarButton.pack(pady=5)

    # Botão Pular
    pularButton = ctk.CTkButton(
        master=frame_botoes,
        text="Pular",
        font=("Inter", 16, "bold"),
        text_color="#EBBFA7",
        fg_color="#A25A31",
        hover_color="#663A20",
        width=200,
        height=40,
        command=pular_login
    )
    pularButton.pack(pady=5)

    janela_login.mainloop()

def abrir_menu():
    janela = ctk.CTk()
    janela.geometry("400x600")
    janela.title("Menu Principal - Pet Shop Management")
    janela.configure(fg_color="#FFEADF")
    janela.resizable(False, False)

    frame_principal = ctk.CTkFrame(janela, fg_color="#D9D9D9")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(frame_principal, text="Menu Principal", font=("Inter", 24, "bold")).pack(pady=20)

    def abrir_tutores():
        janela.withdraw()
        criar_janela_tutores()
        janela.deiconify()

    def abrir_animais():
        janela.withdraw()
        criar_janela_animais()
        janela.deiconify()

    def abrir_agendamentos():
        janela.withdraw()
        criar_janela_agendamentos()
        janela.deiconify()

    def abrir_pagamentos():
        janela.withdraw()
        criar_janela_pagamentos()
        janela.deiconify()

    def abrir_servicos():
        janela.withdraw()
        criar_janela_servicos()
        janela.deiconify()

    botao_style = {"width": 300, "height": 50, "font": ("Inter", 14)}

    # Criar botões
    ctk.CTkButton(frame_principal, text="Gerenciar Tutores", command=abrir_tutores, **botao_style).pack(pady=10)
    ctk.CTkButton(frame_principal, text="Gerenciar Animais", command=abrir_animais, **botao_style).pack(pady=10)
    ctk.CTkButton(frame_principal, text="Gerenciar Agendamentos", command=abrir_agendamentos, **botao_style).pack(pady=10)
    ctk.CTkButton(frame_principal, text="Gerenciar Pagamentos", command=abrir_pagamentos, **botao_style).pack(pady=10)
    ctk.CTkButton(frame_principal, text="Gerenciar Serviços", command=abrir_servicos, **botao_style).pack(pady=10)

    janela.mainloop()
