import pandas as pd
import re
from typing import List, Any, Union, Literal, Optional
import openpyxl as opx
from openpyxl.worksheet.worksheet import Worksheet
from pandas import DataFrame

from requirements.dependencies import COLUMNS, SPECIALIZATIONS


# from requirements.dependencies import COLUMNS


# TODO написать docstring к каждой функции
def main():
    wb = opx.load_workbook("../study_plans/test_plans/09.02.07_51-16-123-2843_11-2023_ИСП.plx.xlsx")

    title_sheet = wb["Титул"]
    plan_sheet = wb["План"]

    entry_year = find_entry_year(sheet=title_sheet)
    group_name = get_group_name(filename="09.02.07_51-16-123-2843_11-2023_ИСП.plx.xlsx", entry_year=entry_year)
    education_form = find_education_form(sheet=title_sheet)
    print("entry year: ", entry_year)
    print("education form: ", education_form)
    first_semester, second_semester = find_semester_boundaries(sheet=plan_sheet, today_year=2024,
                                                               entry_year=int(entry_year))

    disciplines_col = find_disciplines_column(sheet=plan_sheet)
    print("d_col: ", disciplines_col)
    study_load = parse_study_load(sheet=plan_sheet, first_semester=first_semester, second_semester=second_semester,
                                  disciplines_col=disciplines_col)
    format_to_converter(study_load=study_load, group_name=group_name, education_form=education_form)


def check_filenames(files: Any) -> List[str]:
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
            print(f"[+]: {file} валидно")
        else:
            invalid_files.append(file)
            print(f"[ERR]: {file} не валидно")
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


def get_group_name(filename: str, entry_year: int) -> str:
    """Из имени файла извлекается код специальности, база класса,
    и год поступления передается из результата другой функции. В результате формируется имя группы:
    год-сокращение_специальности-класса"""

    data_labels = ["specialization", "fgos_standard", "course_numbers", "class_base", "entry_year"]
    file_name = filename.split("/")[-1]
    file_data_list = file_name.replace("_", "-").rstrip(".").split("-")[:-1]
    file_data_list.pop(1)  # Удаление ненужной части
    file_data_list.remove("2843")  # Удаления кода организации "2843"
    specialization_key = file_data_list[0]
    group_classbase = file_data_list[3]
    group_codename = SPECIALIZATIONS[specialization_key][0]
    group_name = f"{entry_year[-2:]}-{group_codename}-{group_classbase}"
    return group_name


def find_education_form(sheet: Worksheet) -> Optional[str]:
    forms_dict = {"Очная": "ОФО",
                  "Очно-заочная": "ОЗФО",
                  "Заочная": "ЗФО"}
    pattern = re.compile(r'(Очная|очно-заочная|заочная)')
    for row in sheet.iter_rows(min_row=30, max_row=60, values_only=True):
        for cell in row:
            if cell and pattern.search(str(cell)):
                education_form = pattern.search(str(cell)).group(1)
                if education_form in forms_dict:
                    education_form = forms_dict[education_form]
                    return education_form
    return None


def find_entry_year(sheet: Worksheet) -> Optional[int]:
    pattern = re.compile(r"^\d{4}$")
    for row in sheet.iter_rows(min_row=30, max_row=60, values_only=True):
        year_cell = next((cell for cell in row if cell and re.match(pattern, str(cell))), None)
        if year_cell:
            return year_cell
    return None


def find_semester_boundaries(sheet: Worksheet, today_year: int, entry_year: int):
    course_number = today_year - entry_year + 1
    course_boundaries = []
    semester_data = []
    pattern = re.compile(r"^[Кк]урс\s+" + str(course_number))

    for row in sheet.iter_rows(max_row=5):
        for cell in row:
            if isinstance(cell.value, str) and pattern.search(cell.value):
                for merged_range in sheet.merged_cells.ranges:
                    if cell.coordinate in merged_range:
                        course_boundaries.extend([merged_range.min_col, merged_range.max_col, merged_range.min_row,
                                                  merged_range.max_row])
        break

    for row in sheet.iter_rows(min_col=course_boundaries[0], max_col=course_boundaries[1], min_row=course_boundaries[2],
                               max_row=course_boundaries[3] + 1):
        for cell in row:
            if isinstance(cell.value, str) and cell.value.startswith("Семестр"):
                for merged_range in sheet.merged_cells.ranges:
                    if cell.coordinate in merged_range:
                        match = re.search(r'Семестр\s+(\d+)', cell.value)
                        semester_number = int(match.group(1))
                        match = re.search(r'(\d+) нед\]', cell.value)
                        semester_length = int(match.group(1))
                        semester_data.append([merged_range.min_col, merged_range.max_col, merged_range.min_row,
                                              merged_range.max_row, course_number, semester_number, semester_length])

    return semester_data


def find_disciplines_column(sheet: Worksheet) -> int:
    pattern = re.compile(r'Наименование$')
    for row in sheet.iter_rows(min_row=1, max_row=10, max_col=5):
        for cell in row:
            if isinstance(cell.value, str) and pattern.search(cell.value):
                return cell.column


def parse_disciplines(sheet: Worksheet) -> DataFrame:
    data = pd.DataFrame(columns=["Шифр дисциплины", "Наименование дисциплины"])
    pattern = re.compile(r"[а-яА-Я]+\.\d{1,3}")  # https://regex101.com/r/Htwvzy/1

    def is_discipline(cell):
        return cell.value and isinstance(cell.value, str) and pattern.search(cell.value)

    for row in sheet.iter_rows():
        discipline_cell = next((cell for cell in row if is_discipline(cell)), None)
        if not discipline_cell:
            continue
        data.loc[len(data)] = [discipline_cell.value, ""]
        last_idx = len(data) - 1
        next_cell_index = discipline_cell.column + 1
        if next_cell_index <= row[-1].column:
            data.at[last_idx, "Наименование дисциплины"] = row[next_cell_index - 1].value

    return data


def parse_study_load(
        sheet: Worksheet, first_semester: List[int], second_semester: List[int],
        disciplines_col: int) -> List[DataFrame]:
    disciplines_data = []
    first_semester_data = []
    second_semester_data = []
    disciplines_pattern = re.compile(r'[а-яА-Я]+\.\d{1,3}')

    # Парсинг 1 семестра
    for row in sheet.iter_rows(min_col=disciplines_col - 1, max_col=first_semester[1], values_only=False):
        if row[0].value and row[1].value:
            if not row[1].font.bold:
                match = disciplines_pattern.search(row[0].value)
                if match:
                    disciplines_data.append([row[0].value, row[1].value])
                    # Черная магия
                    first_semester_data.append(
                        [row[0].value, first_semester[4], first_semester[5], first_semester[6],
                         *[cell.value for cell in row[first_semester[0] - 2:first_semester[1] + 1]],
                         ])

    # Парсинг 2 семестра
    for row in sheet.iter_rows(min_col=disciplines_col - 1, max_col=second_semester[1], values_only=False):
        if row[0].value and row[1].value:
            if not row[1].font.bold:
                match = disciplines_pattern.search(row[0].value)
                if match:
                    # Черная магия
                    second_semester_data.append(
                        [row[0].value, second_semester[4], second_semester[5], second_semester[6],
                         *[cell.value for cell in row[second_semester[0] - 2:second_semester[1] + 1]],
                         ])

    disciplines_df = pd.DataFrame(disciplines_data,
                                  columns=["Шифр дисциплины", "Наименование дисциплины"])

    first_semester_df = pd.DataFrame(first_semester_data,
                                     columns=["Шифр дисциплины", "Курс", "Семестр",
                                              "Число учебных недель", "Всего часов", "Всего ауд. часов", "Лекции",
                                              "Практические занятия", "КРП",
                                              "ИП", "Консультации", "Сам.работа (по актуализ.ФГОС)", "Экзамены"])
    second_semester_df = pd.DataFrame(second_semester_data,
                                      columns=["Шифр дисциплины", "Курс", "Семестр",
                                               "Число учебных недель", "Всего часов", "Всего ауд. часов", "Лекции",
                                               "Практические занятия", "КРП",
                                               "ИП", "Консультации", "Сам.работа (по актуализ.ФГОС)", "Экзамены"])

    return [disciplines_df, first_semester_df, second_semester_df]


# TODO доделать вторую половину таблицы, понять откуда парсить "Продолжительность практики (нед)",
# TODO спарсить "Форма контроля c листа "План"
def format_to_converter(study_load: List[DataFrame], group_name: str, education_form: str):
    disciplines_df, first_semester_df, second_semester_df = study_load
    print(disciplines_df.to_string())
    print(first_semester_df.to_string())
    print(second_semester_df.to_string())
    cols = pd.DataFrame()
    result = pd.concat([cols, disciplines_df[["Наименование дисциплины", "Шифр дисциплины"]]], axis=1)
    result[COLUMNS[2]] = education_form
    result[COLUMNS[3]] = group_name
    fsem = pd.merge(result[
                        first_semester_df["Всего часов"].notna() | first_semester_df["Всего ауд. часов"].notna() |
                        first_semester_df['Лекции'].notna() | first_semester_df['Практические занятия'].notna() |
                        first_semester_df['КРП'].notna() | first_semester_df['ИП'].notna() |
                        first_semester_df['Консультации'].notna() | first_semester_df['Сам.работа (по актуализ.ФГОС)'].notna() |
                        first_semester_df['Экзамены'].notna()
                        ], first_semester_df, on='Шифр дисциплины')
    ssem = pd.merge(result[
                        second_semester_df["Всего часов"].notna() | second_semester_df["Всего ауд. часов"].notna() |
                        second_semester_df['Лекции'].notna() | second_semester_df['Практические занятия'].notna() |
                        second_semester_df['КРП'].notna() | second_semester_df['ИП'].notna() |
                        second_semester_df['Консультации'].notna() | second_semester_df['Сам.работа (по актуализ.ФГОС)'].notna() |
                        second_semester_df['Экзамены'].notna()
                        ], second_semester_df, on='Шифр дисциплины')

    result = pd.concat([fsem, ssem], ignore_index=True)
    for i in range(6, 9):
        result.insert(loc=i, column=COLUMNS[i], value="")

    result["КРП"] = result["КРП"].fillna(0).astype(int)
    result["ИП"] = result["ИП"].fillna(0).astype(int)
    _ = result["КРП"] + result["ИП"]
    result.assign(КРП=_)
    result = result.rename(columns={"КРП": COLUMNS[17]})
    result = result.drop(["ИП"], axis=1)

    result = result[["Наименование дисциплины", "Шифр дисциплины", "Форма обучения", "Номер группы",
                     "Курс", "Семестр", "Студентов", "Потоков", "Групп",
                     "Число учебных недель",
                     "Лекции", "Практические занятия", "Консультации",
                     "Экзамены", "Сам.работа (по актуализ.ФГОС)", "Курсовые работы / Индивидуальный проект",
                     "Всего ауд. часов", "Всего часов"]]
    print("result\n", result.to_string())


if __name__ == '__main__':
    main()
