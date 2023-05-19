import os
from datetime import date, datetime
import re
from typing import List, Any, Dict, Union

import openpyxl
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet


def main():
    pass



def check_filenames(files: Any) -> list:
    """Проверяет список файлов с которыми мы будем работать на корректность названия

    :param files: Список файлов которые выбрал пользователь
    :type files: List
    :returns: Список файлов прошедших валидацию
    :rtype: list
    """
    valid_files = []
    invalid_files = []
    for file in files:
        if filename_validator(file):
            valid_files.append(file)
            print(f"Имя файла: {file} корректно")
        else:
            invalid_files.append(file)
            print(f"Имя файла: {file} не корректно")
    return valid_files


def filename_validator(filename: str) -> bool:
    """
    # Код.специальности_XXX_стандарт_количество.курсов_XXX_класс_год.набора_специальность
    # regex: d{2}.d{2}.d{2}_d{2}_d{2}_(d{3,4}/d{4})-2843_(d{2})-(d{4})

    :param filename: Имя файла которое будем валидировать
    :type filename: string
    :returns: Значение результата проверки
    :rtype: bool
    """
    if re.search(r"\d{2}\.\d{2}\.\d{2}[_-]\d{2}[_-]\d{2}[_-]\d{2,4}[_-]2843[_-]\d{2}[_-]\d{4}[_-][а-яА-Я]{1,3}",
                 filename):
        return True
    return False


def extract_data_from_filename(filename: str) -> dict[str, int]:
    """
    :param filename:
    :return:
    """

    namings = ["specialization", "fgos_standard", "course_numbers", "class_base", "entry_year"]
    name = filename.split("/")[-1]
    file_data = name.replace("_", "-").rstrip(".").split("-")[:-1]
    file_data.pop(1)  # Удаление ненужной части
    file_data.remove("2843")  # Удаления кода организации "2843"
    if len(file_data) == 5:
        file_dict = dict(zip(namings, file_data))
        return file_dict


def find_entry_year(sheet: Worksheet):
    for row in sheet.iter_rows(min_row=20, max_row=60, values_only=True):
        for cell in row:
            if cell is not None:
                try:
                    if re.search(r"^\d{4}$", str(cell)):
                        return cell
                except Exception as e:
                    print(f"Не был найден год поступления. {e}")


def find_course_boundaries(sheet: Worksheet, today_year: int, entry_year: int) -> Union[List[int], None]:
    course_number = today_year - entry_year + 1
    pattern = r"[а-яА-Я]{4}\s+" + str(course_number)
    try:
        for row in sheet.iter_rows(max_row=5):
            for cell in row:
                if cell.value and isinstance(cell.value, str) and re.search(pattern, cell.value):
                    for merged_range in sheet.merged_cells.ranges:
                        if cell.coordinate in merged_range:
                            return [merged_range.min_col, merged_range.max_col]
    except Exception as e:
        print(f"Границы курса были не найдены. {e}")
    return None


if __name__ == '__main__':
    main()
