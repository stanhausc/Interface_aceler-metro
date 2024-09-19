import customtkinter as ctk
from tkinter import PhotoImage
from Utils.clear_frame import clear_main_frame

def show_contact_info(main_frame):
    clear_main_frame(main_frame)

    contact_frame = ctk.CTkFrame(main_frame)
    contact_frame.pack(pady=20, padx=20, fill='x')

    contact_label = ctk.CTkLabel(master=contact_frame, text="Contato\nEmail: cristian.stanhaus@itaipuparquetec.org.br", font=('Arial', 18))
    contact_label.pack(pady=20)

    try:
        logo = PhotoImage(file="logo.png")
        logo_label = ctk.CTkLabel(master=contact_frame, image=logo, text="")
        logo_label.image = logo
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Erro ao carregar a imagem do logotipo: {e}")
