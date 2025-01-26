import subprocess
import sys
import os
from config import Config  # Імпортуємо клас Config

def run_script(python_exe, script_path):
    """Запускає python скрипт, використовуючи вказаний інтерпретатор."""
    print(f"Запуск {script_path} з інтерпретатором {python_exe}...")
    try:
        subprocess.run([python_exe, script_path], check=True)
        print(f"ВИКОНАННЯ файлу {script_path} УСПІШНО ЗАВЕРШЕНО.\n")
    except subprocess.CalledProcessError as e:
        print(f"ПОМИЛКА ПРИ ВИКОНАННІ {script_path}: {e}\n")
        sys.exit(1)  # Зупиняємо виконання run_all.py у разі помилки

if __name__ == "__main__":
    # Створення об'єкту Config
    config = Config()

    # Запуск скриптів з абсолютними шляхами
    base_path = config.current_dir

    # 1. Створення Excel файлу
    run_script(config.python_exe, os.path.join(base_path, "create_excel_data.py"))

    # 2. Створення БД
    run_script(config.python_exe, os.path.join(base_path, "create_database.py"))

    # 3. Заповнення БД
    run_script(config.python_exe, os.path.join(base_path, "populate_database.py"))

    # 4. Виконання SQL запитів
    run_script(config.python_exe, os.path.join(base_path, "sql_queries.py"))