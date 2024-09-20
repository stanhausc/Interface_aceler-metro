import customtkinter as ctk
from tkinter import messagebox
import threading
from Models.acelerometros import read_acelerometros_from_db, update_acelerometro_names
from Utils.clear_frame import clear_main_frame

# Função para exibir a aba de cadastro
def show_cadastro(main_frame, refresh_all_tabs):
    show_dados_brutos(main_frame)

# Função para exibir a aba de dados brutos
def show_dados_brutos(main_frame):
    clear_main_frame(main_frame)

    # Criar o frame para exibir os dados brutos
    dados_brutos_frame = ctk.CTkFrame(main_frame)
    dados_brutos_frame.pack(pady=20, padx=20, fill='x')

    ctk.CTkLabel(master=dados_brutos_frame, text="Sensores Encontrados", font=('Arial', 18)).grid(row=0, column=0, padx=10, pady=5, sticky='w')

    acelerometro_entries = []

    # Função que será executada em uma thread separada para carregar os acelerômetros
    def carregar_acelerometros():
        # Obter os nomes e o número de acelerômetros do banco de dados
        acelerometro_names, num_sensors = read_acelerometros_from_db()

        # Atualizar a interface gráfica na thread principal
        def update_ui():
            # Exibir os acelerômetros e uma caixa de entrada para renomear ou digitar valores
            for i in range(num_sensors):
                label = ctk.CTkLabel(master=dados_brutos_frame, text=f"Sensor {i+1}: {acelerometro_names[i]}")
                label.grid(row=i+1, column=0, padx=10, pady=5, sticky='w')

                entry = ctk.CTkEntry(master=dados_brutos_frame, placeholder_text="Digite um valor")
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky='w')
                acelerometro_entries.append(entry)

        # Chamar o update_ui na thread principal usando after
        main_frame.after(0, update_ui)

    # Executar a função carregar_acelerometros em uma thread separada
    threading.Thread(target=carregar_acelerometros).start()
