import customtkinter as ctk
from tkinter import PhotoImage, Spinbox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
from tkcalendar import DateEntry
from datetime import datetime, timedelta

# Configuração básica do tema e aparência
ctk.set_appearance_mode("Dark")  # Modo de aparência escura
ctk.set_default_color_theme("blue")  # Tema de cor azul

def fetch_sensor_data(start_date=None, end_date=None):
    try:
        connection = sqlite3.connect('sensors.db')
        cursor = connection.cursor()

        query = "SELECT timestamp, sensor1_value, sensor2_value, sensor3_value FROM sensor_data"
        params = ()

        # Filtrar por data se as datas de início e fim forem fornecidas
        if start_date and end_date:
            query += " WHERE timestamp BETWEEN ? AND ?"
            params = (start_date, end_date)

        cursor.execute(query, params)
        data = cursor.fetchall()
        connection.close()

        # Tentar converter o timestamp com milissegundos e sem milissegundos
        def parse_timestamp(ts):
            try:
                return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f')  # Tenta com milissegundos
            except ValueError:
                return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')  # Tenta sem milissegundos

        # Aplicar a conversão de timestamp usando a função parse_timestamp
        data = [(parse_timestamp(row[0]), row[1], row[2], row[3]) for row in data]

        return data
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return []
    except ValueError as ve:
        print(f"Erro ao converter timestamp: {ve}")
        return []

# Função para mostrar os dados dos sensores em tempo real
def show_sensor_data():
    clear_main_frame()
    
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20, padx=20, fill='x')

    sensor1_label = ctk.CTkLabel(master=frame, text="Sensor 1: ---", font=('Arial', 18))
    sensor1_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    sensor2_label = ctk.CTkLabel(master=frame, text="Sensor 2: ---", font=('Arial', 18))
    sensor2_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    sensor3_label = ctk.CTkLabel(master=frame, text="Sensor 3: ---", font=('Arial', 18))
    sensor3_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

    # Função para atualizar os valores dos sensores na interface
    def update_sensor_values():
        data = fetch_sensor_data()
        if data:
            _, sensor1_value, sensor2_value, sensor3_value = data[-1]
            sensor1_label.configure(text=f"Sensor 1: {sensor1_value:.2f}")
            sensor2_label.configure(text=f"Sensor 2: {sensor2_value:.2f}")
            sensor3_label.configure(text=f"Sensor 3: {sensor3_value:.2f}")
        main_frame.after(1000, update_sensor_values)  # Atualiza a cada 1000 ms (1 segundo)
    
    update_sensor_values()

# Função para limpar o frame principal sem destruir todos os widgets desnecessariamente
def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.pack_forget()

# Função para mostrar o gráfico com base nas seleções do usuário
def show_graph():
    clear_main_frame()
    
    date_frame = ctk.CTkFrame(master=main_frame)
    date_frame.pack(pady=10, padx=20, fill='x')

    # Data Inicial
    ctk.CTkLabel(master=date_frame, text="Data Inicial:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
    start_date_entry = DateEntry(master=date_frame, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    start_date_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

    # Hora Inicial
    ctk.CTkLabel(master=date_frame, text="Hora Inicial:", font=('Arial', 14)).grid(row=0, column=2, padx=10, pady=5, sticky='w')
    start_hour_entry = Spinbox(master=date_frame, from_=0, to=23, width=3, format='%02.0f')  # Horas
    start_hour_entry.grid(row=0, column=3, padx=5)
    start_minute_entry = Spinbox(master=date_frame, from_=0, to=59, width=3, format='%02.0f')  # Minutos
    start_minute_entry.grid(row=0, column=4, padx=5)

    # Data Final
    ctk.CTkLabel(master=date_frame, text="Data Final:", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
    end_date_entry = DateEntry(master=date_frame, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    end_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

    # Hora Final
    ctk.CTkLabel(master=date_frame, text="Hora Final:", font=('Arial', 14)).grid(row=1, column=2, padx=10, pady=5, sticky='w')
    end_hour_entry = Spinbox(master=date_frame, from_=0, to=23, width=3, format='%02.0f')  # Horas
    end_hour_entry.grid(row=1, column=3, padx=5)
    end_minute_entry = Spinbox(master=date_frame, from_=0, to=59, width=3, format='%02.0f')  # Minutos
    end_minute_entry.grid(row=1, column=4, padx=5)

    sensor_frame = ctk.CTkFrame(master=main_frame)
    sensor_frame.pack(pady=10, padx=20, fill='x')

    sensor1_var = ctk.IntVar(value=1)
    sensor2_var = ctk.IntVar(value=1)
    sensor3_var = ctk.IntVar(value=1)

    sensor1_checkbox = ctk.CTkCheckBox(master=sensor_frame, text="Sensor 1", variable=sensor1_var)
    sensor1_checkbox.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    sensor2_checkbox = ctk.CTkCheckBox(master=sensor_frame, text="Sensor 2", variable=sensor2_var)
    sensor2_checkbox.grid(row=0, column=1, padx=10, pady=5, sticky='w')

    sensor3_checkbox = ctk.CTkCheckBox(master=sensor_frame, text="Sensor 3", variable=sensor3_var)
    sensor3_checkbox.grid(row=0, column=2, padx=10, pady=5, sticky='w')

    # Placeholder para o gráfico
    graph_canvas = None

    def plot_graph():
        nonlocal graph_canvas  # Para permitir modificar a variável graph_canvas dentro da função
        
        # Construção dos timestamps completos com horas e minutos
        start_date = start_date_entry.get_date().strftime('%Y-%m-%d')
        start_time = f"{int(start_hour_entry.get()):02d}:{int(start_minute_entry.get()):02d}:00"
        start_timestamp = f"{start_date} {start_time}"

        end_date = end_date_entry.get_date().strftime('%Y-%m-%d')
        end_time = f"{int(end_hour_entry.get()):02d}:{int(end_minute_entry.get()):02d}:59"
        end_timestamp = f"{end_date} {end_time}"

        data = fetch_sensor_data(start_timestamp, end_timestamp)
        if not data:
            print("Nenhum dado encontrado para o intervalo selecionado.")
            if graph_canvas:  # Se existir um gráfico, remove-o
                graph_canvas.get_tk_widget().pack_forget()
            return

        timestamps, sensor1_values, sensor2_values, sensor3_values = zip(*data)
        fig, ax = plt.subplots(figsize=(10, 5))

        plot_any_data = False

        if sensor1_var.get():
            ax.plot(timestamps, sensor1_values, label='Sensor 1', marker='o', linestyle='-', color='blue')
            plot_any_data = True
        if sensor2_var.get():
            ax.plot(timestamps, sensor2_values, label='Sensor 2', marker='x', linestyle='-', color='green')
            plot_any_data = True
        if sensor3_var.get():
            ax.plot(timestamps, sensor3_values, label='Sensor 3', marker='s', linestyle='-', color='red')
            plot_any_data = True

        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Sensor Values')
        ax.set_title('Vibration Sensor Data')
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))

        if plot_any_data:
            ax.legend(loc='upper left', fontsize='small')

        # Remove o gráfico anterior, se existir
        if graph_canvas:
            graph_canvas.get_tk_widget().pack_forget()

        graph_canvas = FigureCanvasTkAgg(fig, master=main_frame)  
        graph_canvas.draw()
        graph_canvas.get_tk_widget().pack(pady=20, fill='both', expand=True)

    # Botão para atualizar o gráfico com as novas seleções
    update_button = ctk.CTkButton(master=main_frame, text="Atualizar Tendências", command=plot_graph, height=40, width=200, font=('Arial', 14))
    update_button.pack(pady=20)

    # Inicializa o gráfico com as configurações padrões
    plot_graph()

# Função para mostrar informações de contato
def show_contact_info():
    clear_main_frame()
    
    contact_label = ctk.CTkLabel(master=main_frame, text="Contato\nEmail: cristian.stanhaus@itaipuparquetec.org.br", font=('Arial', 18))
    contact_label.pack(pady=20)

    try:
        logo = PhotoImage(file="logo.png")  # Certifique-se de ter uma imagem 'logo.png'
        logo_label = ctk.CTkLabel(master=main_frame, image=logo, text="")
        logo_label.image = logo  # Manter referência para evitar garbage collection
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Erro ao carregar a imagem do logotipo: {e}")

# Função para cancelar a atualização ao fechar a aplicação
def on_closing():
    root.destroy()

# Criar a janela principal
root = ctk.CTk()
root.geometry("1000x700")  # Define o tamanho da janela
root.title("Vibration Sensor Data Viewer")  # Define o título da janela

# Criar barra lateral
sidebar_frame = ctk.CTkFrame(root, width=200, corner_radius=0)
sidebar_frame.pack(side="left", fill="y")

# Botões da barra lateral
home_button = ctk.CTkButton(sidebar_frame, text="Dados Brutos", command=show_sensor_data)
home_button.pack(pady=10, padx=10)

graph_button = ctk.CTkButton(sidebar_frame, text="Tendências", command=show_graph)
graph_button.pack(pady=10, padx=10)

contact_button = ctk.CTkButton(sidebar_frame, text="Contato", command=show_contact_info)
contact_button.pack(pady=10, padx=10)

# Frame principal para exibir o conteúdo das abas
main_frame = ctk.CTkFrame(root)
main_frame.pack(side="right", fill="both", expand=True)

# Exibir a aba inicial com os dados dos sensores
show_sensor_data()

# Vincula a função de fechamento para garantir que o after seja cancelado corretamente
root.protocol("WM_DELETE_WINDOW", on_closing)

# Rodar a interface
root.mainloop()
