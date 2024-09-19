import customtkinter as ctk  # Importar customtkinter como ctk
from Models.acelerometros import read_acelerometros_from_db, fetch_sensor_data
from Utils.clear_main_frame import clear_main_frame  # Importar a função para limpar o frame

def show_acelerometro_data(main_frame):
    # Limpar o conteúdo do frame principal
    clear_main_frame(main_frame)
    
    # Obter os nomes e o número de acelerômetros do banco de dados
    acelerometro_names, num_sensors = read_acelerometros_from_db()

    # Verificar se existem acelerômetros no banco de dados
    if num_sensors == 0:
        no_data_label = ctk.CTkLabel(master=main_frame, text="Nenhum acelerômetro encontrado.", font=('Arial', 18))
        no_data_label.pack(pady=20)
        return  # Encerrar a função se não houver dados

    # Criar o frame para exibir os dados
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20, padx=20, fill='x')

    # Inicializar uma lista para manter os labels dos acelerômetros
    acelerometro_labels = []

    # Função para atualizar os valores dos acelerômetros em tempo real
    def update_acelerometro_values():
        # Obter os dados do sensor
        data = fetch_sensor_data()

        if data:
            # Exibir os últimos valores obtidos para o número de acelerômetros encontrados
            timestamp, *sensor_values = data[-1]
            
            # Limpar labels antigos
            for label in acelerometro_labels:
                label.pack_forget()
            
            acelerometro_labels.clear()

            # Atualizar apenas os acelerômetros que têm dados
            for i, value in enumerate(sensor_values[:num_sensors]):
                acelerometro_label = ctk.CTkLabel(master=frame, text=f"{acelerometro_names[i]}: {value:.2f}", font=('Arial', 18))
                acelerometro_label.pack(padx=10, pady=5)
                acelerometro_labels.append(acelerometro_label)
        
        # Agendar a próxima atualização em 1 segundo
        main_frame.after(1000, update_acelerometro_values)

    # Iniciar a atualização dos valores
    update_acelerometro_values()

