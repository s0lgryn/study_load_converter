import tkinter as tk
from tkinter import ttk
from gui.functions import update_progress, select_files, delete_file


root = tk.Tk()
root.resizable(width=False, height=False)
root.title("Конвертер")
root.iconbitmap("convert.ico")

# Создаем прогресс-бар
progress = ttk.Progressbar(root, length=350, mode='determinate')
progress.grid(row=0, column=0, padx=10, pady=10)
# Cоздаем список файлов
listbox = tk.Listbox(root)
listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

select_button = tk.Button(root, text="Выбрать файлы", command=select_files, width=15)
select_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

delete_button = tk.Button(root, text="Удалить", command=delete_file, width=15)
delete_button.grid(row=2, column=0, padx=10, pady=10, sticky="n")

start_button = tk.Button(root, text="Начать", width=15)
start_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")

root.mainloop()
