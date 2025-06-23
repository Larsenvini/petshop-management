from tkinter import messagebox
import customtkinter as ctk
from tkinter import *
from PIL import Image
from main import abrir_menu 

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
        janela.destroy()
        abrir_menu()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

ctk.set_appearance_mode("light")

janela = ctk.CTk()
janela.geometry("500x500")
janela.iconbitmap("assets/icon.ico")
janela.title("Painel de Login")
janela.resizable(False, False)
janela.configure(fg_color="#FFEADF")

loginText = ctk.CTkLabel(
    master=janela,
    text="Login",
    font=("Inter", 36, "bold"),
    text_color="#A25A31"
)
loginText.place(x=201, y=128)

user_pil = Image.open("assets/user.png")
user_img = ctk.CTkImage(light_image=user_pil, size=(24, 24))  # tamanho do ícone

password_pil = Image.open("assets/password.png")
password_img = ctk.CTkImage(light_image=password_pil, size=(24, 24))  # tamanho do ícone

entradaUsuario_frame = ctk.CTkFrame(
    master=janela,
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

password_pil = Image.open("assets/password.png")
password_img = ctk.CTkImage(light_image=password_pil, size=(24, 24))

entradaSenha_frame = ctk.CTkFrame(
    master=janela,
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

entrarButton = ctk.CTkButton(
    master=janela,
    text="Entrar",
    font=("Inter", 16, "bold"),
    text_color="#EBBFA7",
    fg_color="#A25A31",
    hover_color="#663A20",
    width=234,
    height=41,
    corner_radius=50,
    command=realizar_login
)
entrarButton.place(x=133, y=290)


janela.mainloop()
