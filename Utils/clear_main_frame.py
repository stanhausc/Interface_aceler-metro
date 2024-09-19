def clear_main_frame(main_frame):
    """
    Função para limpar o frame principal sem destruir os widgets.
    """
    for widget in main_frame.winfo_children():
        widget.pack_forget()
