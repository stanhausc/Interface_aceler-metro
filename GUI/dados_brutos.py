import customtkinter as ctk
from Models.acelerometros import read_acelerometros_from_db, fetch_sensor_data
from Utils.clear_main_frame import clear_main_frame

def show_acelerometro_data(main_frame):
    clear_main_frame(main_frame)
    
    acelerometro_names, num_sensors = read_acelerometros_from_db()

    if num_sensors == 0:
        no_data_label = ctk.CTkLabel(master=main_frame, text="Nenhum acelerômetro encontrado.", font=('Arial', 18))
        no_data_label.pack(pady=20)
        return

    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20, padx=20, fill='x')

    acelerometro_labels = []

    def update_acelerometro_values():
        start_timestamp = "2024-09-19 00:00:00"  # Defina adequadamente os timestamps
        end_timestamp = "2024-09-20 23:59:59"
        
        data = fetch_sensor_data(start_timestamp, end_timestamp)

        if data:
            timestamp, *sensor_values = data[-1]
            
            for label in acelerometro_labels:
                label.pack_forget()
            
            acelerometro_labels.clear()

            for i, value in enumerate(sensor_values[:num_sensors]):
                acelerometro_label = ctk.CTkLabel(master=frame, text=f"{acelerometro_names[i]}: {value:.2f}", font=('Arial', 18))
                acelerometro_label.pack(padx=10, pady=5)
                acelerometro_labels.append(acelerometro_label)

        main_frame.after(1000, update_acelerometro_values)

    update_acelerometro_values()