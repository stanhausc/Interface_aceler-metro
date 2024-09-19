import customtkinter as ctk
from tkinter import messagebox
import threading
from Models.acelerometros import read_acelerometros_from_db, update_acelerometro_names
from Utils.clear_frame import clear_main_frame

# Função para exibir a aba de cadastro
def show_cadastro(main_frame, refresh_callback):
    clear_main_frame(main_frame)

    # Criar o frame para cadastro
    cadastro_frame = ctk.CTkFrame(main_frame)
    cadastro_frame.pack(pady=20, padx=20, fill='x')

    ctk.CTkLabel(master=cadastro_frame, text="Renomear Acelerômetros", font=('Arial', 18)).grid(row=0, column=0, padx=10, pady=5, sticky='w')

    acelerometro_entries = []

    # Função que será executada em uma thread separada para carregar os acelerômetros
    def carregar_acelerometros():
        # Obter os nomes e o número de acelerômetros do banco de dados
        acelerometro_names, num_sensors = read_acelerometros_from_db()

        # Atualizar a interface gráfica na thread principal
        def update_ui():
            # Gerar os campos de entrada para renomear os acelerômetros
            for i in range(num_sensors):
                entry = ctk.CTkEntry(master=cadastro_frame, placeholder_text=f"Nome atual: {acelerometro_names[i]}")
                entry.grid(row=i+1, column=0, padx=10, pady=5, sticky='w')
                acelerometro_entries.append(entry)

            # Botão para atualizar o cadastro
            modbus_button = ctk.CTkButton(master=cadastro_frame, text="Atualizar Cadastro", command=update_cadastro)
            modbus_button.grid(row=num_sensors+2, column=0, padx=10, pady=20)

            leitura_button = ctk.CTkButton(master=cadastro_frame, text="Recarregar Nomes", command=lambda: show_cadastro(main_frame, refresh_callback))
            leitura_button.grid(row=num_sensors+3, column=0, padx=10, pady=20)

        # Chamar o update_ui na thread principal usando after
        main_frame.after(0, update_ui)

    # Função para atualizar os nomes dos acelerômetros
    def update_cadastro():
        new_names = [entry.get() if entry.get() else acelerometro_names[i] for i, entry in enumerate(acelerometro_entries)]
        update_acelerometro_names(new_names)
        messagebox.showinfo("Cadastro Atualizado", "Nomes atualizados com sucesso!")
        # Chamar a função de atualização das outras abas
        refresh_callback()

    # Executar a função carregar_acelerometros em uma thread separada
    threading.Thread(target=carregar_acelerometros).start()
