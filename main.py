import customtkinter as ctk
import sys
import os

# Adiciona o diretório principal ao sys.path para que os módulos das pastas sejam encontrados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importação das funcionalidades de cada aba
from GUI.tendencias import show_graph
from GUI.erros import show_errors
from GUI.dados_brutos import show_acelerometro_data
from GUI.contact import show_contact_info

# Criar a janela principal
root = ctk.CTk()
root.geometry("1000x700")
root.title("Vibration Acelerômetro Data Viewer")

# Criar barra lateral
sidebar_frame = ctk.CTkFrame(root, width=200, corner_radius=0)
sidebar_frame.pack(side="left", fill="y")

# Frame principal para exibir o conteúdo das abas
main_frame = ctk.CTkFrame(root)
main_frame.pack(side="right", fill="both", expand=True)

# Função para atualizar as abas "Dados Brutos" e "Tendências"
def refresh_all_tabs():
    # Atualiza a aba de dados brutos
    show_acelerometro_data(main_frame)
    # Atualiza a aba de tendências
    show_graph(main_frame)

# Botões da barra lateral
home_button = ctk.CTkButton(sidebar_frame, text="Dados Brutos", command=lambda: show_acelerometro_data(main_frame))
home_button.pack(pady=10, padx=10)

graph_button = ctk.CTkButton(sidebar_frame, text="Tendências", command=lambda: show_graph(main_frame))
graph_button.pack(pady=10, padx=10)

error_button = ctk.CTkButton(sidebar_frame, text="Erros", command=lambda: show_errors(main_frame))
error_button.pack(pady=10, padx=10)

contact_button = ctk.CTkButton(sidebar_frame, text="Contato", command=lambda: show_contact_info(main_frame))
contact_button.pack(pady=10, padx=10)

# Exibir a aba inicial com os dados dos acelerômetros
show_acelerometro_data(main_frame)

root.mainloop()
 