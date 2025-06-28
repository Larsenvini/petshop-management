import customtkinter as ctk
from database.db_config import inicializar_banco
from crud.tutores import criar_janela_tutores
from crud.animais import criar_janela_animais
from crud.servicos import criar_janela_servicos
from crud.agendamentos import criar_janela_agendamentos
from crud.pagamentos import criar_janela_pagamentos

def login():
    def verificar_login():
        usuario = entrada_usuario.get()
        senha = entrada_senha.get()
        
        if usuario == "admin" and senha == "123":
            janela_login.destroy()
            menu_principal()
        else:
            ctk.CTkLabel(janela_login, text="Usuário ou senha incorretos!", 
                        text_color="red").pack(pady=5)
    
    janela_login = ctk.CTk()
    janela_login.geometry("400x300")
    janela_login.title("Login - Pet Shop")
    janela_login.configure(fg_color="#FFEADF")
    
    ctk.CTkLabel(janela_login, text="Pet Shop Management", 
                 font=("Arial", 24, "bold")).pack(pady=30)
    
    frame_login = ctk.CTkFrame(janela_login, fg_color="#D9D9D9")
    frame_login.pack(pady=20, padx=40, fill="both", expand=True)
    
    ctk.CTkLabel(frame_login, text="Usuário:").pack(pady=10)
    entrada_usuario = ctk.CTkEntry(frame_login, width=200)
    entrada_usuario.pack(pady=5)
    
    ctk.CTkLabel(frame_login, text="Senha:").pack(pady=10)
    entrada_senha = ctk.CTkEntry(frame_login, width=200, show="*")
    entrada_senha.pack(pady=5)
    
    ctk.CTkButton(frame_login, text="Entrar", command=verificar_login, 
                  width=200).pack(pady=20)
    
    janela_login.mainloop()

def menu_principal():
    janela = ctk.CTk()
    janela.geometry("600x500")
    janela.title("Pet Shop - Menu Principal")
    janela.configure(fg_color="#FFEADF")
    
    ctk.CTkLabel(janela, text="Sistema de Gestão Pet Shop", 
                 font=("Arial", 28, "bold")).pack(pady=30)
    
    frame_botoes = ctk.CTkFrame(janela, fg_color="#D9D9D9")
    frame_botoes.pack(pady=30, padx=50, fill="both", expand=True)
    
    ctk.CTkButton(frame_botoes, text="Gerenciar Tutores", 
                  command=criar_janela_tutores, height=50, 
                  font=("Arial", 16)).pack(pady=10, padx=20, fill="x")
    
    ctk.CTkButton(frame_botoes, text="Gerenciar Animais", 
                  command=criar_janela_animais, height=50, 
                  font=("Arial", 16)).pack(pady=10, padx=20, fill="x")
    
    ctk.CTkButton(frame_botoes, text="Gerenciar Serviços", 
                  command=criar_janela_servicos, height=50, 
                  font=("Arial", 16)).pack(pady=10, padx=20, fill="x")
    
    ctk.CTkButton(frame_botoes, text="Gerenciar Agendamentos", 
                  command=criar_janela_agendamentos, height=50, 
                  font=("Arial", 16)).pack(pady=10, padx=20, fill="x")
    
    ctk.CTkButton(frame_botoes, text="Gerenciar Pagamentos", 
                  command=criar_janela_pagamentos, height=50, 
                  font=("Arial", 16)).pack(pady=10, padx=20, fill="x")
    
    ctk.CTkButton(frame_botoes, text="Sair", command=janela.quit, 
                  height=50, font=("Arial", 16), 
                  fg_color="#FF6B6B").pack(pady=20, padx=20, fill="x")
    
    janela.mainloop()

if __name__ == "__main__":
    inicializar_banco()
    login()