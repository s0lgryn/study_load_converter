import os.path
import time
import tkinter as tk
from tkinter import ttk, filedialog


class Converter(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        # Задаем параметры окну
        self.resizable(width=False, height=False)
        self.title("Конвертер")
        self.iconbitmap("convert.ico")
        # Создаем список выбранных файлов
        self.files_list = []
        # Создаем переменную для хранения значения прогресса
        self.progress_value = tk.DoubleVar()
        # Создаем виджеты
        self.progress = ttk.Progressbar(self, length=350, mode='determinate', variable=self.progress_value)
        self.listbox = tk.Listbox(self, )
        self.label = tk.Label(self, text="Файлов выбрано: 0")
        self.select_button = tk.Button(self, text="Выбрать файлы", command=self.select_files, width=15)
        self.delete_button = tk.Button(self, text="Удалить", command=self.delete_file, width=15)
        self.start_button = tk.Button(self, text="Начать", command=self.start_processing, width=15)

        # Размещаем виджеты на экране
        self.progress.grid(row=0, column=0, padx=10, pady=10)
        self.listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.select_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.delete_button.grid(row=3, column=0, padx=10, pady=10, sticky="n")
        self.start_button.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    def select_files(self):
        files = filedialog.askopenfilenames()
        self.listbox.delete(0, tk.END)  # Очистка списка перед добавлением новых файлов
        for file in files:
            self.files_list.append(file)
            name = os.path.basename(file)
            self.listbox.insert(tk.END, name)
        self.label.config(text=f"Файлов выбрано: {self.listbox.size()}")
        self.label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    def delete_file(self):
        index = self.listbox.curselection()[0]

        del self.files_list[index]
        self.listbox.delete(index)
        self.label.config(text=f"Файлов выбрано: {self.listbox.size()}")

    def update_progress(self):
        current_value = self.progress_value.get()
        if current_value > 100:
            self.progress_value.set(0)
            current_value = 0
        self.progress_value.set(current_value + (100 / self.listbox.size()))
        self.update_idletasks()

    def start_processing(self):
        for file in self.files_list:
            time.sleep(1)
            self.update_progress()


app = Converter()
app.grid()
app.mainloop()