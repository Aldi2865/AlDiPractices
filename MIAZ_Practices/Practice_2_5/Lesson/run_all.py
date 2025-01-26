import subprocess
import sys
import os

def find_venv(start_path):
  """Шукає .venv в поточному та батьківських каталогах."""
  current_path = start_path
  while True:
    venv_path = os.path.join(current_path, ".venv")
    if os.path.isdir(venv_path):
      return venv_path
    parent_path = os.path.dirname(current_path)
    if parent_path == current_path:  # Досягли кореня диску
      return None
    current_path = parent_path

def run_script(python_exe, script_path):
  """Запускає python скрипт, використовуючи вказаний інтерпретатор."""
  print(f"Running {script_path} with {python_exe}...")
  try:
    subprocess.run([python_exe, script_path], check=True)
    print(f"Finished {script_path} successfully.\n")
  except subprocess.CalledProcessError as e:
    print(f"Error running {script_path}: {e}\n")

if __name__ == "__main__":
  # Пошук .venv, починаючи з каталогу, де знаходиться run_all.py
  current_dir = os.path.dirname(os.path.abspath(__file__))
  venv_path = find_venv(current_dir)

  if venv_path:
    # Знайдено .venv
    python_exe = os.path.join(venv_path, "Scripts", "python.exe")  # Windows
    # python_exe = os.path.join(venv_path, "bin", "python")  # macOS/Linux

    # Перевірка чи існує інтерпретатор
    if not os.path.exists(python_exe):
        print(f"Помилка: Інтерпретатор Python не знайдено у {python_exe}")
        sys.exit(1)

    # Запуск скриптів
    base_path = os.path.join(current_dir) # Шлях до папки Practice_2_5
    
    run_script(python_exe, os.path.join(base_path, "create_database.py"))
    run_script(python_exe, os.path.join(base_path, "populate_database.py"))
    run_script(python_exe, os.path.join(base_path, "sql_queries.py"))
  else:
    print("Помилка: Не знайдено віртуальне середовище .venv")
    sys.exit(1)