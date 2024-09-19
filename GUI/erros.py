import customtkinter as ctk
from Utils.clear_frame import clear_main_frame
from Models.logs import error_log

def show_errors(main_frame):
    clear_main_frame(main_frame)

    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20, padx=20, fill='x')

    error_list_label = ctk.CTkLabel(master=frame, text="Log de Erros", font=('Arial', 18))
    error_list_label.pack(pady=10)

    for error in error_log:
        error_label = ctk.CTkLabel(master=frame, text=error, font=('Arial', 14))
        error_label.pack(anchor="w", padx=20, pady=2)
