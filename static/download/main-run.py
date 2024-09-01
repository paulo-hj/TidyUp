import os
import shutil
import re
from tkinter import *
import tkinter as tk
import tkinter.filedialog as fd
import customtkinter
from PIL import Image, ImageTk
import webbrowser

class Func:
    def variaveis(self):
        self.quantoDigitos = 14
        self.indicadorRev = "rev"

    def teclaEnterOrganizar(self, event):
        self.organizar()

    def limparOrganizar(self):
        self.entradaOrganizar.delete(0, END)
        self.label_mensagem.pack_forget()

    def mostrar_mensagem(self, mensagem, cor):
        self.label_mensagem.configure(text=mensagem, text_color=cor)
        self.label_mensagem.place(relx=0.5, rely=0.75, anchor=CENTER)

    def organizar(self):
        diretorio_origem = self.entradaOrganizar.get()
        if not os.path.isdir(diretorio_origem):
            self.mostrar_mensagem("Diretório inválido!", "red")
            return
        
        arquivos = os.listdir(diretorio_origem)
        pastas_criadas = {}
        alteracoes_feitas = False

        try:
            for arquivo in arquivos:
                caminho_arquivo = os.path.join(diretorio_origem, arquivo)
                
                if os.path.isfile(caminho_arquivo):
                    nome_base = arquivo[:self.quantoDigitos]
                    if nome_base not in pastas_criadas:
                        novo_diretorio = os.path.join(diretorio_origem, nome_base)
                        if not os.path.exists(novo_diretorio):
                            os.makedirs(novo_diretorio)
                            #print(f"Criando diretório: {novo_diretorio}")
                            alteracoes_feitas = True
                        else:
                            #print(f"Diretório {novo_diretorio} já existe.")
                            pass
                        pastas_criadas[nome_base] = novo_diretorio
                    
                    match = re.search(fr'{self.indicadorRev}\s*([a-zA-Z\d]+)', arquivo[self.quantoDigitos:], re.IGNORECASE)
                    if match:
                        subdir_name = f"Rev.{match.group(1)}"
                        subdir_path = os.path.join(pastas_criadas[nome_base], subdir_name)
                        if not os.path.exists(subdir_path):
                            os.makedirs(subdir_path)
                            #print(f"Criando subdiretório: {subdir_path}")
                            alteracoes_feitas = True
                        destino = subdir_path
                    else:
                        match_rev = re.search(fr'{self.indicadorRev}\s*(\d+)', arquivo[self.quantoDigitos:], re.IGNORECASE)
                        if match_rev:
                            subdir_name = f"Rev.{match_rev.group(1)}"
                            subdir_path = os.path.join(pastas_criadas[nome_base], subdir_name)
                            if not os.path.exists(subdir_path):
                                os.makedirs(subdir_path)
                                #print(f"Criando subdiretório: {subdir_path}")
                                alteracoes_feitas = True
                            destino = subdir_path
                        else:
                            destino = pastas_criadas[nome_base]
                    
                    #print(f"Movendo arquivo {arquivo} para {destino}")
                    shutil.move(caminho_arquivo, destino)
                    alteracoes_feitas = True

            if alteracoes_feitas:
                self.mostrar_mensagem("Arquivos organizados com sucesso!", "green")
            else:
                self.mostrar_mensagem("Nenhuma alteração realizada.", "yellow")
        except Exception as e:
            self.mostrar_mensagem(f"Erro: {str(e)}", "red")


    def buscarPasta(self):
        diretorio = fd.askdirectory()
        if diretorio:
            self.entradaOrganizar.delete(0, END)
            self.entradaOrganizar.insert(0, diretorio)

    def abrir_github(self, event):
        webbrowser.open_new("https://github.com/paulo-hj")

class Interface:
    def tela(self):
        primeiraTela = customtkinter.CTk()
        primeiraTela.geometry("600x400+900+400")
        primeiraTela.resizable(width=False, height=False)
        primeiraTela.title("Organizador de Arquivos")
        primeiraTela.configure(bg="#062F4F")
        icon_path = "logo1.ico"
        #primeiraTela.iconbitmap(icon_path)
        self.primeiraTela = primeiraTela
        self.widgetsPrimeiraTela()
        primeiraTela.mainloop()

    def widgetsPrimeiraTela(self):
        self.primeiraTela.bind('<Return>', self.teclaEnterOrganizar)

        logo_image = Image.open("hgbsoft.png")
        logo_image = logo_image.resize((150, 150), Image.LANCZOS)  # Redimensiona a imagem para 150x150
        ctk_logo_image = customtkinter.CTkImage(light_image=logo_image, dark_image=logo_image, size=(150, 150))
        logo_label = customtkinter.CTkLabel(self.primeiraTela, image=ctk_logo_image, text="")
        logo_label.place(relx=0.5, rely=0.13, anchor=CENTER)

        label = customtkinter.CTkLabel(
            self.primeiraTela, 
            text="Informe o caminho da pasta no servidor",
            text_color="white",
            font=("Helvetica", 15, "bold")
        )
        #label.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.entradaOrganizar = customtkinter.CTkEntry(self.primeiraTela, placeholder_text="                            Informe o caminho da pasta", height=30, width=350)
        self.entradaOrganizar.place(relx=0.79, rely=0.4, anchor=E)
        self.entradaOrganizar.focus()

        botaoBuscarPasta = customtkinter.CTkButton(
            self.primeiraTela, 
            text="Pesquisar", 
            command=self.buscarPasta, 
            font=("Helvetica", 12, "bold"),
            height=30,
            width=85
        )
        botaoBuscarPasta.place(relx=0.816, rely=0.4, anchor=W)

        botaoConectarOrganizar = customtkinter.CTkButton(
            self.primeiraTela, 
            text="Organizar", 
            command=self.organizar, 
            font=("Helvetica", 12, "bold"),
            height=40,
            width=100
        )
        botaoConectarOrganizar.bind('<Enter>', lambda e: botaoConectarOrganizar.configure(cursor="hand2"))
        botaoConectarOrganizar.place(relx=0.5, rely=0.65, anchor=CENTER)

        # Cria a label para mensagens de erro/sucesso, inicialmente invisível
        self.label_mensagem = customtkinter.CTkLabel(self.primeiraTela, text="", font=("Helvetica", 12))
        self.label_mensagem.pack_forget()
        self.label_mensagem.place(relx=0.5, rely=0.75, anchor=CENTER)

        botaoLimparOrganizar = customtkinter.CTkButton(
            self.primeiraTela, 
            text="Limpar", 
            command=self.limparOrganizar, 
            font=("Helvetica", 12, "bold"),
            height=30,
            width=80,
        )
        #botaoLimparOrganizar.place(relx=0.5, rely=0.75, anchor=CENTER)

        botaoSobre = customtkinter.CTkButton(
            self.primeiraTela, 
            text="Sobre", 
            command=self.telaSobre, 
            font=("Helvetica", 12, "bold"),
            height=30,
            width=80
        )
        botaoSobre.place(relx=0.95, rely=0.95, anchor=SE)

    def telaSobre(self):
        janela_sobre = tk.Toplevel(self.primeiraTela)
        janela_sobre.title("Sobre")
        janela_sobre.resizable(width=False, height=False)
        x_pos = 980 + (600 - 480) // 2
        y_pos = 450 + (400 - 360) // 2
        janela_sobre.geometry(f"{480}x360+{x_pos}+{y_pos}")
        icon_path = "logo1.ico"
        #janela_sobre.iconbitmap(icon_path)
        cor_fundo = self.primeiraTela.cget("bg")
        janela_sobre.configure(bg=cor_fundo)
        janela_sobre.tk_setPalette(background=cor_fundo)

        # Adicionando o texto explicativo sobre a aplicação
        texto_explicativo = (
            "Esta aplicação foi projetada para organizar arquivos dentro de pastas. "
            "Ela filtra os primeiros 14 caracteres do nome de cada arquivo para criar"
            "uma pasta correspondente e, em seguida, move os arquivos para essas pastas."
        )
        explicativo_label = customtkinter.CTkLabel(janela_sobre, text=texto_explicativo, font=("Helvetica", 12), wraplength=350, justify="left")
        explicativo_label.place(relx=0.05, rely=0.05, anchor=NW)

        linha = customtkinter.CTkLabel(janela_sobre, text="__________________________________________________________________________________", font=("Helvetica", 12, "bold"))
        linha.place(relx=0, rely=0.25, anchor=NW)

        desenvolvedores_label = customtkinter.CTkLabel(janela_sobre, text="Desenvolvedores", font=("Helvetica", 12, "bold"))
        desenvolvedores_label.place(relx=0.05, rely=0.35, anchor=NW)

        desenvolvedor1_label = customtkinter.CTkLabel(janela_sobre, text="Paulo Henrique", font=("Helvetica", 12))
        desenvolvedor1_label.place(relx=0.05, rely=0.43, anchor=NW)

        desenvolvedor2_label = customtkinter.CTkLabel(janela_sobre, text="Silas Vinicius", font=("Helvetica", 12))
        desenvolvedor2_label.place(relx=0.05, rely=0.5, anchor=NW)

        contato_label = customtkinter.CTkLabel(janela_sobre, text="Contatos", font=("Helvetica", 12, "bold"))
        contato_label.place(relx=0.578, rely=0.35, anchor=NW)

        email_label = customtkinter.CTkLabel(janela_sobre, text="paulo.junior.ph@gmail.com", font=("Helvetica", 12))
        email_label.place(relx=0.578, rely=0.43, anchor=NW)

        codigo_label = customtkinter.CTkLabel(janela_sobre, text="Código Fonte", font=("Helvetica", 12, "bold"))
        codigo_label.place(relx=0.05, rely=0.66, anchor=NW)

        github_label_text = "GitHub"
        github_label = customtkinter.CTkLabel(janela_sobre, text=github_label_text, font=("Helvetica", 12), cursor="hand2")
        github_label.place(relx=0.05, rely=0.74, anchor=NW)
        github_label.bind("<Button-1>", self.abrir_github)

        v1_label = customtkinter.CTkLabel(janela_sobre, text="Versão da aplicação", font=("Helvetica", 12, "bold"))
        v1_label.place(relx=0.578, rely=0.66, anchor=NW)

        versao_label = customtkinter.CTkLabel(janela_sobre, text="1.0", font=("Helvetica", 12))
        versao_label.place(relx=0.578, rely=0.74, anchor=NW)

        janela_sobre.transient(self.primeiraTela)
        janela_sobre.grab_set()

        janela_sobre.mainloop()

class Main(Func, Interface):
    def __init__(self):
        self.tela()

Main()
