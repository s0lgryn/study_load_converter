import os
from copy import copy

import openpyxl
from openpyxl.writer.excel import save_workbook
from requirements.dependencies import DATA_DIR, FILENAME, TODAY_YEAR, NEXT_YEAR

HEADER = "requirements/header.xlsx"
RESULT_FILENAME = f"{FILENAME}_{TODAY_YEAR}-{NEXT_YEAR}.xlsx"

# Если директории нет мы ее создаем
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
    print(f"{DATA_DIR}{RESULT_FILENAME}")


# Если в директории лежит файл мы его открываем, иначе создаем новую книгу
try:
    wb = openpyxl.load_workbook(f"{DATA_DIR}/{RESULT_FILENAME}")
except FileNotFoundError:
    wb = openpyxl.Workbook()

# Удаляем лист, который создается по дефолту
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    wb.remove(sheet)


# TODO копирует только Merged ячейки
# Создаем лист с необходимым названием
ws = wb.create_sheet(f"Тарификация {TODAY_YEAR}-{NEXT_YEAR}")
header = openpyxl.load_workbook(HEADER)['header']
for group in list(header.merged_cells.ranges):
    min_col, min_row, max_col, max_row = group.bounds
    cell_start = header.cell(row=min_row, column=min_col)
    top_left_cell_value = cell_start.value

    for i_row in range(min_row, max_row + 1):
        for j_col in range(min_col, max_col + 1):
            ws.cell(row=i_row, column=j_col, value=top_left_cell_value)
            # Копирование стилей
            ws.cell(row=i_row, column=j_col).alignment = copy(cell_start.alignment)
            ws.cell(row=i_row, column=j_col).border = copy(cell_start.border)
            ws.cell(row=i_row, column=j_col).font = copy(cell_start.font)
            ws.cell(row=i_row, column=j_col).fill = copy(cell_start.fill)
    ws.merge_cells(start_column=min_col, start_row=min_row, end_column=max_col, end_row=max_row)
save_workbook(wb, f"{DATA_DIR}/{RESULT_FILENAME}")
