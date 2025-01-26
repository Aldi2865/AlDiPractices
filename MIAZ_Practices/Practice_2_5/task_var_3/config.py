import os
import sys

class Config:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))  # Визначаємо директорію, де знаходиться config.py
        self.db_name = "MIAZ2025_Practice2_5"
        self.user = "postgres"
        self.password = "admin"
        self.host = "localhost"
        self.port = "5432"
        self.excel_file = os.path.join(self.current_dir, "operations_data.xlsx") # Відносний шлях від директорії з config.py
        self.venv_path = self.find_venv()
        self.python_exe = self.get_python_exe()

    def find_venv(self):
        """Шукає .venv в поточному та батьківських каталогах."""
        start_path = self.current_dir
        current_path = start_path
        while True:
            venv_path = os.path.join(current_path, ".venv")
            if os.path.isdir(venv_path):
                return venv_path
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:  # Досягли кореня диску
                return None
            current_path = parent_path

    def get_python_exe(self):
        """Повертає шлях до інтерпретатора Python у віртуальному середовищі, або системний інтерпретатор, якщо .venv не знайдено."""
        if self.venv_path:
            # Windows
            python_exe = os.path.join(self.venv_path, "Scripts", "python.exe")
            # macOS/Linux
            # python_exe = os.path.join(self.venv_path, "bin", "python")
            if os.path.exists(python_exe):
                return python_exe
        # Якщо .venv не знайдено, або інтерпретатор у .venv не існує, повертаємо системний інтерпретатор
        print("Увага: .venv не знайдено. Використовується системний інтерпретатор Python.")
        return sys.executable