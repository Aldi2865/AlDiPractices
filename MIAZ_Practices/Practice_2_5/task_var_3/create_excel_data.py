import pandas as pd
import os
import random
from faker import Faker
from config import Config
import time

def create_operations_data_excel(config):
    """Створює файл Excel з даними для операцій та персоналу (по 100 записів)."""
    file_path = config.excel_file
    fake = Faker()

    # Дані для листа Operations
    operations_data = {
        'Operation_ID': range(1, 101),
        'Operation_Name': [f"Operation {fake.word().capitalize()}" for _ in range(100)],
        'Commander': [f"{random.choice(['Maj.', 'Capt.'])} {fake.last_name()}" for _ in range(100)],
        'Operation_Start_Date': [fake.date_between(start_date='-30d', end_date='+30d') for _ in range(100)],
        'Operation_End_Date': [fake.date_between(start_date='+31d', end_date='+60d') for _ in range(100)]
    }
    operations_df = pd.DataFrame(operations_data)

    # Дані для листа Operations_Staff
    staff_data = {
        'ID': range(1, 101),
        'Name': [fake.name() for _ in range(100)],
        'Role': [random.choice(['Analyst', 'Coordinator', 'Operator', 'Engineer', 'Medic']) for _ in range(100)],
        'Operation_ID': [random.randint(1, 100) for _ in range(100)],
        'Date_Assigned': [fake.date_between(start_date='-20d', end_date='-1d') for _ in range(100)]
    }
    staff_df = pd.DataFrame(staff_data)

    # Створення файлу Excel
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        operations_df.to_excel(writer, sheet_name='Operations', index=False)
        staff_df.to_excel(writer, sheet_name='Operations_Staff', index=False)

    # Додаємо затримку в 1 секунду для уникнення помилки відсутності файлу при виконанні
    time.sleep(1)
    print(f"'operations_data.xlsx' було створено у {file_path} з 100 тестовими записами")

if __name__ == "__main__":
    # Створення об'єкту Config
    config = Config()

    print(f"Використовується інтерпретатор: {config.python_exe}")
    create_operations_data_excel(config)