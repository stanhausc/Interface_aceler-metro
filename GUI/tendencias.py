import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import Spinbox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
from Models.acelerometros import fetch_sensor_data, fetch_severity_data, fetch_envelope_data  # Corrigido para fetch_sensor_data
from Utils.clear_main_frame import clear_main_frame

def show_graph(main_frame):
    clear_main_frame(main_frame)
    
    date_frame = ctk.CTkFrame(master=main_frame)
    date_frame.pack(pady=10, padx=20, fill='x')

    # Data Inicial
    ctk.CTkLabel(master=date_frame, text="Data Inicial:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
    start_date_entry = DateEntry(master=date_frame, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    start_date_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

    # Hora Inicial
    ctk.CTkLabel(master=date_frame, text="Hora Inicial:", font=('Arial', 14)).grid(row=0, column=2, padx=10, pady=5, sticky='w')
    start_hour_entry = Spinbox(master=date_frame, from_=0, to=23, width=3, format='%02.0f')
    start_hour_entry.grid(row=0, column=3, padx=5)
    start_minute_entry = Spinbox(master=date_frame, from_=0, to=59, width=3, format='%02.0f')
    start_minute_entry.grid(row=0, column=4, padx=5)

    # Data Final
    ctk.CTkLabel(master=date_frame, text="Data Final:", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
    end_date_entry = DateEntry(master=date_frame, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    end_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

    # Hora Final
    ctk.CTkLabel(master=date_frame, text="Hora Final:", font=('Arial', 14)).grid(row=1, column=2, padx=10, pady=5, sticky='w')
    end_hour_entry = Spinbox(master=date_frame, from_=0, to=23, width=3, format='%02.0f')
    end_hour_entry.grid(row=1, column=3, padx=5)
    end_minute_entry = Spinbox(master=date_frame, from_=0, to=59, width=3, format='%02.0f')
    end_minute_entry.grid(row=1, column=4, padx=5)

    # Reorganizar os ticks: Severidade e Envelope primeiro
    severity_var = ctk.IntVar(value=1)
    severity_checkbox = ctk.CTkCheckBox(master=main_frame, text="Severidade de Vibração", variable=severity_var)
    severity_checkbox.pack(pady=10)

    envelope_var = ctk.IntVar(value=1)
    envelope_checkbox = ctk.CTkCheckBox(master=main_frame, text="Envelope de Aceleração", variable=envelope_var)
    envelope_checkbox.pack(pady=10)

    # Acelerômetros abaixo de Severidade e Envelope
    acelerometro_vars = []
    acelerometro_frame = ctk.CTkFrame(master=main_frame)
    acelerometro_frame.pack(pady=10, padx=20, fill='x')

    for i, name in enumerate(["Acelerômetro 1", "Acelerômetro 2", "Acelerômetro 3"]):
        var = ctk.IntVar(value=1)
        acelerometro_vars.append(var)
        acelerometro_checkbox = ctk.CTkCheckBox(master=acelerometro_frame, text=name, variable=var)
        acelerometro_checkbox.grid(row=i, column=0, padx=10, pady=5, sticky='w')

    graph_canvas = None

    def plot_graph():
        nonlocal graph_canvas

        # Capturar os valores de data e hora
        start_date = start_date_entry.get_date().strftime('%Y-%m-%d')
        start_time = f"{start_hour_entry.get()}:{start_minute_entry.get()}:00"
        end_date = end_date_entry.get_date().strftime('%Y-%m-%d')
        end_time = f"{end_hour_entry.get()}:{end_minute_entry.get()}:59"
        
        # Formatar timestamps
        start_timestamp = f"{start_date} {start_time}"
        end_timestamp = f"{end_date} {end_time}"

        # Buscar dados do banco de dados
        acelerometro_data = fetch_sensor_data(start_timestamp, end_timestamp)
        severity_data = fetch_severity_data(start_timestamp, end_timestamp)
        envelope_data = fetch_envelope_data(start_timestamp, end_timestamp)

        # Plotagem dos gráficos (você pode expandir esta seção com base nos dados retornados)
        if graph_canvas:
            graph_canvas.get_tk_widget().pack_forget()  # Remover gráfico anterior

        fig, ax = plt.subplots(figsize=(10, 5))

        if acelerometro_data:
            timestamps, sensor1_values, sensor2_values, sensor3_values = zip(*acelerometro_data)
            ax.plot(timestamps, sensor1_values, label='Acelerômetro 1', marker='o', color='blue')
            ax.plot(timestamps, sensor2_values, label='Acelerômetro 2', marker='x', color='green')
            ax.plot(timestamps, sensor3_values, label='Acelerômetro 3', marker='s', color='red')

        if severity_var.get() and severity_data:
            severity_timestamps, severity_values = zip(*severity_data)
            ax.plot(severity_timestamps, severity_values, label='Severidade de Vibração', marker='D', linestyle='--', color='purple')

        if envelope_var.get() and envelope_data:
            envelope_timestamps, envelope_values = zip(*envelope_data)
            ax.plot(envelope_timestamps, envelope_values, label='Envelope de Aceleração', marker='v', linestyle='--', color='orange')

        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Values')
        ax.legend(loc='upper left', fontsize='small')
        ax.grid(True)

        fig.autofmt_xdate(rotation=45)
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))

        graph_canvas = FigureCanvasTkAgg(fig, master=main_frame)
        graph_canvas.draw()
        graph_canvas.get_tk_widget().pack(pady=20, fill='both', expand=True)

    # Botão para atualizar o gráfico com as novas seleções
    update_button = ctk.CTkButton(master=main_frame, text="Atualizar Tendências", command=plot_graph, height=40, width=200, font=('Arial', 14))
    update_button.pack(pady=20)

    plot_graph()