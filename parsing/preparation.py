import os
from datetime import date

import openpyxl
from openpyxl.writer.excel import save_workbook
from requirements.dependencies import DATA_DIR, FILENAME


def main():
    check_is_dir_exists()
    check_is_file_exist()


def check_is_dir_exists() -> None:
    """Проверяет, существует ли директория из переменной DATA_DIR, если нет то создает её"""
    if not os.path.exists(f"../{DATA_DIR}"):
        os.mkdir(f"../{DATA_DIR}")


def check_is_file_exist() -> None:
    # TODO написать нормальный коммент
    """Проверяет, существует ли в директории DATA_DIR, файл формата: FIlENAME_ТекущийГод_СледующийГод.
    Если файла нет, то он копирует шапку из requirements/header.xlsx и создает файл в папке converter
    """
    today_year = date.today().year
    next_year = date.today().year + 1
    path_to_header = "../requirements/header.xlsx"
    result_filename = f"{FILENAME}_{today_year}-{next_year}.xlsx"
    try:
        openpyxl.load_workbook(f"{DATA_DIR}/{result_filename}")
    except FileNotFoundError:
        # Перемещаем шапку в новую папку и даем листу корректное название
        header = openpyxl.load_workbook(path_to_header)  # Загружаем лист с шапкой
        _sheet = header.active  # Выбираем лист
        new_sheet = header.copy_worksheet(_sheet)  # Создаем его копию
        new_sheet.title = f"Тарификация {today_year}-{next_year}"  # Копии листа присваиваем новое имя
        header.remove(_sheet)  # Убираем лист со старым названием
        save_workbook(header, f"../{DATA_DIR}/{result_filename}")  # Сохраняем файл по новому адресу


if __name__ == '__main__':
    main()
