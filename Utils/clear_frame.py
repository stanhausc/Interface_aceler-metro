def clear_main_frame(main_frame):
    for widget in main_frame.winfo_children():
        widget.pack_forget()
