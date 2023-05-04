# Testing GUI, still in progress

import tkinter

import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk()
app.geometry("400x440")


def button_fun():
    print("button pressed")


button = customtkinter.CTkButton(master=app, text="Test button", command=button_fun)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

app.mainloop()
