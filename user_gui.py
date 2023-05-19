# Testing GUI, still in progress
import os
import re
import tkinter
from tkinter import filedialog

from customtkinter import CTkProgressBar

from document_parser import check_filenames
import customtkinter


class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item,)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=1, padx=10, pady=5)
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x500")
        self.title("CTkScrollableFrame example")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        def get_files_from_user():
            filenames = filedialog.askopenfilenames()
            if filenames != "":
                files = check_filenames(filenames)
                for file in files:
                    self.scrollable_checkbox_frame.add_item(file)

        # create scrollable checkbox frame
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=700, label_text="Список файлов",
                                                                 command=self.checkbox_frame_event,
                                                                 item_list=[])
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

        self.choose_files = customtkinter.CTkButton(master=self, text="Выберите файлы", command=get_files_from_user)
        self.choose_files.grid(row=0, column=1, padx=15, pady=15)

        self.delete = customtkinter.CTkButton(master=self, text="Удалить", command=get_files_from_user)
        self.delete.grid(row=0, column=2, padx=15, pady=15)

    def checkbox_frame_event(self):
        print(f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()

