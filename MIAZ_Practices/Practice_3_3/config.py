import os

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