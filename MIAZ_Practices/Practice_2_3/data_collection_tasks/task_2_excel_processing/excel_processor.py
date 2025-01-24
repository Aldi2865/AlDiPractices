import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path


def filter_excel_data(input_file, output_file, date_column, condition_months=1):
    """
    Читає дані з таблиці Excel, фільтрує їх за датою (за останній місяць)
    і зберігає відфільтровані дані у новий Excel-файл.

    Args:
        input_file (str): Шлях до вхідного Excel-файлу.
        output_file (str): Шлях до вихідного Excel-файлу.
        date_column (str): Назва колонки з датами.
        condition_months (int): Кількість місяців для фільтрації (за замовчуванням 1 - останній місяць).
    """

    try:
        # Зчитуємо дані з Excel
        df = pd.read_excel(input_file)

        # Перетворюємо колонку з датами у формат datetime
        df[date_column] = pd.to_datetime(df[date_column])

        # Визначаємо початкову дату для фільтрації
        end_date = df[date_column].max()
        print(end_date)
        start_date = datetime(year=end_date.year, month=end_date.month, day=1)  # перший день останнього місяця         print(start_date)
        # Фільтруємо дані за умовою
        filtered_df = df[
            (df[date_column] >= start_date) & (df[date_column] <= end_date)
        ]

        # Зберігаємо відфільтровані дані у новий Excel-файл
        filtered_df.to_excel(output_file, index=False)

        print(f"Дані успішно відфільтровано та збережено у файл '{output_file}'")

    except FileNotFoundError:
        print(f"Помилка: Файл '{input_file}' не знайдено.")
    except KeyError:
        print(f"Помилка: У файлі '{input_file}' відсутня колонка '{date_column}'.")
    except Exception as e:
        print(f"Сталася помилка: {e}")


        # Використання:
directory = os.path.dirname(__file__)
input_f_name = "data.xlsx"
output_f_name = "filtered_data.xlsx"
input_file = directory / input_f_name
output_file = directory / output_f_name
date_column = "Date"  # Замініть на назву колонки з датами

# фільтрування даних та збереження результату у новий файл
filter_excel_data(input_file, output_file, date_column)