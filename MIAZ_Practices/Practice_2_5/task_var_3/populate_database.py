import psycopg2
import pandas as pd
from psycopg2 import sql
from config import Config  # Імпортуємо клас Config

def populate_database(config):
    """Заповнює базу даних даними з файлу Excel."""
    conn = None  # Ініціалізуємо conn
    try:
        conn = psycopg2.connect(database=config.db_name, user=config.user, password=config.password, host=config.host, port=config.port)
        cursor = conn.cursor()

        # Завантаження даних з Excel
        operations_df = pd.read_excel(config.excel_file, sheet_name='Operations')
        staff_df = pd.read_excel(config.excel_file, sheet_name='Operations_Staff')

        # Запис даних у таблицю Operations
        for index, row in operations_df.iterrows():
            cursor.execute(
                sql.SQL("INSERT INTO Operations (Operation_ID, Operation_Name, Commander, Operation_Start_Date, Operation_End_Date) VALUES (%s, %s, %s, %s, %s)"),
                (row['Operation_ID'], row['Operation_Name'], row['Commander'], row['Operation_Start_Date'], row['Operation_End_Date'])
            )

        # Запис даних у таблицю Operations_Staff
        for index, row in staff_df.iterrows():
            cursor.execute(
                sql.SQL("INSERT INTO Operations_Staff (ID, Name, Role, Operation_ID, Date_Assigned) VALUES (%s, %s, %s, %s, %s)"),
                (row['ID'], row['Name'], row['Role'], row['Operation_ID'], row['Date_Assigned'])
            )

        conn.commit()
        cursor.close()

    except psycopg2.Error as e:
        print(f"Помилка при роботі з PostgreSQL: {e}")
    except FileNotFoundError:
        print(f"Помилка: Файл {config.excel_file} не знайдено.")
        exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Створення об'єкту Config
    config = Config()

    print(f"Використовується інтерпретатор: {config.python_exe}")
    populate_database(config)