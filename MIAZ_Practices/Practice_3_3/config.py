import os
import shutil

class Config:
    """
    Клас для зберігання конфігураційних параметрів.
    """
    def __init__(self):
        """
        Ініціалізує об'єкт Config і встановлює шляхи.
        """
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.dataset_directory = os.path.join(self.current_directory, "DataSet")
        self.results_directory = os.path.join(self.current_directory, "results")
        self.setup_results_directory()  # Створюємо або очищуємо папку results при ініціалізації

    def get_current_directory(self):
        """
        Повертає шлях до поточної папки виконання коду.

        Returns:
            str: Шлях до поточної папки виконання коду.
        """
        return self.current_directory

    def get_dataset_directory(self):
        """
        Повертає шлях до папки з датасетом.

        Returns:
            str: Шлях до папки з датасетом.
        """
        return self.dataset_directory

    def get_results_directory(self):
        """
        Повертає шлях до папки з результатами.

        Returns:
            str: Шлях до папки з результатами.
        """
        return self.results_directory

    def clear_results_directory(self):
        """
        Очищає папку з результатами від попередньо створених файлів.
        """
        if os.path.exists(self.results_directory):
            for filename in os.listdir(self.results_directory):
                file_path = os.path.join(self.results_directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Не вдалося видалити {file_path}. Причина: {e}")

    def setup_results_directory(self):
        """
        Створює папку для результатів, якщо її немає, або очищує її, якщо вона існує.
        """
        if not os.path.exists(self.results_directory):
            os.makedirs(self.results_directory)
        else:
            self.clear_results_directory()