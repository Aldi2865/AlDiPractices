import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path


def filter_excel_data(input_file, output_file, date_column, value_column, condition_months=1):
    """
    Читає дані з таблиці Excel, фільтрує їх за датою та значенням
    і зберігає відфільтровані дані у новий Excel-файл.

    Args:
        input_file (str або Path): Шлях до вхідного Excel-файлу.
        output_file (str або Path): Шлях до вихідного Excel-файлу.
        date_column (str): Назва колонки з датами.
        value_column (str): Назва колонки зі значеннями для фільтрації.
        condition_months (int): Кількість місяців для фільтрації (за замовчуванням 1 - останній місяць).
    """

    try:
        # Зчитуємо дані з Excel
        df = pd.read_excel(input_file)

        # Перетворюємо колонку з датами у формат datetime
        df[date_column] = pd.to_datetime(df[date_column])

        # Визначаємо початкову дату для фільтрації
        end_date = df[date_column].max()
        start_date = end_date - relativedelta(months=condition_months - 1, day=1)

        # Фільтруємо дані за датою
        filtered_df = df[
            (df[date_column] >= start_date) & (df[date_column] <= end_date)
        ]

        # Перевірка на порожній DataFrame після фільтрації за датою
        if filtered_df.empty:
            print(
                f"За вказаний період ({start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}) дані відсутні."
            )
            return

        # Запитуємо у користувача порогове значення
        while True:
            try:
                threshold = float(input(f"Введіть порогове значення для колонки '{value_column}': "))
                break
            except ValueError:
                print("Введено некоректне значення. Будь ласка, введіть число.")

        # Запитуємо у користувача тип фільтрації
        while True:
            filter_type = input("Вивести значення, що 'більші' чи 'менші' за порогове? (Введіть 'більші' або 'менші'): ").lower()
            if filter_type in ["більші", "менші"]:
                break
            else:
                print("Некоректний тип фільтрації. Введіть 'більші' або 'менші'.")

        # Фільтруємо дані за значенням
        if filter_type == "більші":
            filtered_df = filtered_df[filtered_df[value_column] > threshold]
        else:  # filter_type == "менші"
            filtered_df = filtered_df[filtered_df[value_column] < threshold]

        # Перевірка на порожній DataFrame після фільтрації за значенням
        if filtered_df.empty:
            print(
                f"За вказаний період та умовою '{value_column} {filter_type} {threshold}' дані відсутні."
            )
            return

        # Зберігаємо відфільтровані дані у новий Excel-файл
        filtered_df.to_excel(output_file, index=False)

        print(f"Дані успішно відфільтровано та збережено у файл '{output_file}'")
        print(f"Період фільтрації: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
        print(f"Умова фільтрації: '{value_column} {filter_type} {threshold}'")

    except FileNotFoundError:
        print(f"Помилка: Файл '{input_file}' не знайдено.")
    except KeyError as e:
        print(f"Помилка: У файлі '{input_file}' відсутня колонка {e}.")
    except Exception as e:
        print(f"Сталася помилка: {e}")


# Використання:
directory = Path(__file__).parent
input_f_name = "data.xlsx"
output_f_name = "filtered_by_user_data.xlsx"
input_file = directory / input_f_name
output_file = directory / output_f_name
date_column = "Date"
value_column = "Value"  # Замініть на назву колонки зі значеннями

# Фільтрування даних за останні 3 місяці з урахуванням введеного користувачем порогового значення та типу фільтра
filter_excel_data(input_file, output_file, date_column, value_column, condition_months=1)