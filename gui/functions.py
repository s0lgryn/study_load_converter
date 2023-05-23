import os
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilenames
import window as w


def update_progress(file_num, num_files):
    w.progress['value'] = (file_num / num_files) * 100
    w.root.update_idletasks()


# Определяем функцию для выбора файлов
def select_files():
    files = askopenfilenames()
    for file in files:
        file = os.path.basename(file)
        w.listbox.insert(tk.END, file)


# Определяем функцию для удаления файлов
def delete_file():
    w.listbox.delete(w.listbox.curselection())


# Запускаем программу
def start_processing():
    pass
