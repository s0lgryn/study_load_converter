import datetime
import re
from typing import List

from openpyxl.worksheet.worksheet import Worksheet


def main():
    filename = [
        "43.02.14-1234-2843-09-2021_ГД.osf", "44.02.04_52-14-1234-2843-09-2019_СДО.osf.plx",
        "21.02.19_51-22-1234-2843_09-2023_ЗУ.plx", "40.02.02_51-14-1234-2843-11-2023_ПД.plx",
        "38.02.06-123-2843-09-2021_ФИН.osf", "40.02.03-51-14-12-2843-11-2022_ПСА.osf.xls"
    ]
    valid_names = (filename_validator(filename))
    for name in valid_names:
        extract_data_from_filename(name)
    invalid_names = list(set(filename) - set(valid_names))  # Получаем разницу между списками, для
    print(valid_names)
    print(invalid_names)


def filename_validator(filenames: list) -> List:
    """
    Код.специальности_XXX_стандарт_количество.курсов_XXX_класс_год.набора_специальность
    00.00.00_51_(16/18/22)_(123/1234)-2843_(09/11)-(2020-2099)_(ПКС/ПД/ЗУ).(osf.xls,plx)
    Принимает список имен файлов
    Возвращает валидный список имен
    :param filenames:
    :return list of valid names:
    """

    valid_names = []
    for name in filenames:
        if re.search(r"\d{2}\.\d{2}\.\d{2}[_-]\d{2}[_-]\d{2}[_-]\d{2,4}[_-]2843[_-]\d{2}[_-]\d{4}[_-]", name):
            valid_names.append(name)
    return valid_names


def extract_data_from_filename(filename: str) -> List:
    """

    :param filename:
    :return:
    """
    file_data = filename.replace("_", "-").rstrip(".").split("-")[:-1]
    file_data.pop(1)  # Удаление ненужной части
    file_data.pop(3)  # Удаления кода организации "2843"
    specialization, fgos_standard, course_numbers, class_, year = file_data
    print(specialization, fgos_standard, course_numbers, class_, year)
    return file_data


def find_course(sheet: Worksheet, today_date: datetime):
    pass


if __name__ == '__main__':
    main()
