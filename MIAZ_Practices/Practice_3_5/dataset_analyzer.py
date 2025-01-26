import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from config import Config  # Змінено імпорт

class DatasetAnalyzer:
    """
    Клас для аналізу та обробки набору даних.
    """

    def __init__(self, config):
        """
        Ініціалізує об'єкт DatasetAnalyzer.

        Args:
            config (Config): Об'єкт конфігурації.
        """
        self.config = config
        self.df_commitments = None
        self.df_allocations = None

    def load_data(self):
        """
        Завантажує дані з CSV файлів у DataFrame.
        """
        commitments_path = self.config.get_dataset_directory() + "/Financial Commitments.csv"
        allocations_path = self.config.get_dataset_directory() + "/Financial Allocations.csv"

        try:
            self.df_commitments = pd.read_csv(commitments_path)
            self.df_allocations = pd.read_csv(allocations_path)
            print("Дані успішно завантажено.")
        except FileNotFoundError:
            print(f"Помилка: Файли не знайдено в {self.config.get_dataset_directory()}.")
            exit()

    def preview_data(self):
        """
        Виводить перші рядки та загальну інформацію про датафрейми.
        """
        print("\nПерші рядки 'Financial Commitments.csv':")
        print(self.df_commitments.head())
        print("\nІнформація про 'Financial Commitments.csv':")
        print(self.df_commitments.info())

        print("\nПерші рядки 'Financial Allocations.csv':")
        print(self.df_allocations.head())
        print("\nІнформація про 'Financial Allocations.csv':")
        print(self.df_allocations.info())

    def clean_data(self):
        """
        Очищує дані: перевіряє на пропущені значення, заповнює їх нулями, видаляє дублікати.
        """
        print("\nПропущені значення в 'Financial Commitments.csv':")
        print(self.df_commitments.isnull().sum())
        print("\nПропущені значення в 'Financial Allocations.csv':")
        print(self.df_allocations.isnull().sum())

        # Заповнення пропущених значень нулями
        self.df_commitments.fillna(0, inplace=True)
        self.df_allocations.fillna(0, inplace=True)

        print("\nПропущені значення заповнено нулями.")

        # Видалення дублікатів
        self.df_commitments.drop_duplicates(inplace=True)
        self.df_allocations.drop_duplicates(inplace=True)
        print("\nДублікати видалено.")

    def transform_data(self):
        """
        Трансформує дані: нормалізує числові дані та перетворює категоріальні. Зберігає результат у файли.
        """
        # Нормалізація числових змінних для 'Financial Commitments.csv'
        numerical_cols_commitments = ['GDP in 2021($ billion)', 'Financial commitments($ billion)',
                                     'Humanitarian commitments($ billion)', 'Military commitments($ billion)',
                                     'Total bilateral commitments($ billion)', 'Share in EU commitments($ billion)',
                                     'Specific weapons and equipment($ billion)',
                                     'Financial commitments with military purpose($ billion)',
                                     'Total bilateral commitments of short term($ billion)']

        scaler = MinMaxScaler()
        self.df_commitments[numerical_cols_commitments] = scaler.fit_transform(
            self.df_commitments[numerical_cols_commitments])

        # Нормалізація числових змінних для 'Financial Allocations.csv'
        numerical_cols_allocations = ['Financial allocations($ billion)', 'Humanitarian allocations($ billion)',
                                       'Military allocations($ billion)', 'Total bilateral allocations($ billion)',
                                       'Share in EU allocations($ billion)']

        self.df_allocations[numerical_cols_allocations] = scaler.fit_transform(
            self.df_allocations[numerical_cols_allocations])

        # One-Hot Encoding для категоріальної змінної 'EU member'
        self.df_commitments = pd.get_dummies(self.df_commitments, columns=['EU member'], prefix=['EU_member'])
        self.df_allocations = pd.get_dummies(self.df_allocations, columns=['EU member'], prefix=['EU_member'])

        print("\nДані трансформовано (нормалізовано числові та застосовано One-Hot Encoding).")

        # Збереження результатів трансформації у файли
        self.df_commitments.to_csv(self.config.get_results_directory() + "/transformed_commitments.csv", index=False)
        self.df_allocations.to_csv(self.config.get_results_directory() + "/transformed_allocations.csv", index=False)
        print(f"\nРезультати трансформації збережено у {self.config.get_results_directory()}.")

    def decompose_data(self):
        """
        Розділяє дані на навчальну та тестову вибірки, проводить кореляційний аналіз та зберігає вибірки у файли.
        """
        # Видалення нечислових стовпців перед поділом
        df_commitments_numeric = self.df_commitments.select_dtypes(include=['number'])
        df_allocations_numeric = self.df_allocations.select_dtypes(include=['number'])


        # Поділ на навчальну та тестову вибірки
        self.train_commitments, self.test_commitments = train_test_split(
            df_commitments_numeric, test_size=0.2, random_state=42)
        self.train_allocations, self.test_allocations = train_test_split(
            df_allocations_numeric, test_size=0.2, random_state=42)

        print("\nДані розділено на навчальну та тестову вибірки.")

        # Збереження навчальної та тестової вибірки у файли
        self.train_commitments.to_csv(self.config.get_results_directory() + "/train_commitments.csv", index=False)
        self.test_commitments.to_csv(self.config.get_results_directory() + "/test_commitments.csv", index=False)
        self.train_allocations.to_csv(self.config.get_results_directory() + "/train_allocations.csv", index=False)
        self.test_allocations.to_csv(self.config.get_results_directory() + "/test_allocations.csv", index=False)
        print(f"\nНавчальну та тестову вибірки збережено у {self.config.get_results_directory()}.")

        # Кореляційний аналіз
        correlation_matrix_commitments = self.train_commitments.corr()
        correlation_matrix_allocations = self.train_allocations.corr()

        print("\nКореляційна матриця для 'Financial Commitments.csv':")
        print(correlation_matrix_commitments)
        print("\nКореляційна матриця для 'Financial Allocations.csv':")
        print(correlation_matrix_allocations)

        # Зберігаємо кореляційні матриці у файли
        correlation_matrix_commitments.to_csv(self.config.get_results_directory() + "/correlation_matrix_commitments.csv")
        correlation_matrix_allocations.to_csv(self.config.get_results_directory() + "/correlation_matrix_allocations.csv")
        print(f"\nКореляційні матриці збережено у {self.config.get_results_directory()}.")

    def descriptive_statistics_and_visualization(self):
        """
        Виконує описову статистику та будує графіки для аналізу даних.
        """
        # Описова статистика
        print("\nОписова статистика для 'Financial Commitments.csv':")
        print(self.df_commitments.describe())
        print("\nОписова статистика для 'Financial Allocations.csv':")
        print(self.df_allocations.describe())

        # Зберігаємо описову статистику у файли
        self.df_commitments.describe().to_csv(self.config.get_results_directory() + "/descriptive_statistics_commitments.csv")
        self.df_allocations.describe().to_csv(self.config.get_results_directory() + "/descriptive_statistics_allocations.csv")
        print(f"\nОписова статистика збережена у {self.config.get_results_directory()}.")

        # Візуалізація
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df_commitments['Total bilateral commitments($ billion)'], bins=20, kde=True)
        plt.title('Розподіл загальних двосторонніх зобов\'язань')
        plt.xlabel('Загальні двосторонні зобов\'язання ($ billion)')
        plt.ylabel('Частота')
        plt.savefig(self.config.get_results_directory() + "/histogram_commitments.png")
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.histplot(self.df_allocations['Total bilateral allocations($ billion)'], bins=20, kde=True)
        plt.title('Розподіл загальних двосторонніх асигнувань')
        plt.xlabel('Загальні двосторонні асигнування ($ billion)')
        plt.ylabel('Частота')
        plt.savefig(self.config.get_results_directory() + "/histogram_allocations.png")
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.df_commitments['Military commitments($ billion)'])
        plt.title('Коробкова діаграма військових зобов\'язань')
        plt.xlabel('Військові зобов\'язання ($ billion)')
        plt.savefig(self.config.get_results_directory() + "/boxplot_commitments.png")
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.df_allocations['Military allocations($ billion)'])
        plt.title('Коробкова діаграма військових асигнувань')
        plt.xlabel('Військові асигнування ($ billion)')
        plt.savefig(self.config.get_results_directory() + "/boxplot_allocations.png")
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=self.df_commitments['Financial commitments($ billion)'],
                        y=self.df_commitments['Military commitments($ billion)'])
        plt.title('Діаграма розсіювання фінансових та військових зобов\'язань')
        plt.xlabel('Фінансові зобов\'язання ($ billion)')
        plt.ylabel('Військові зобов\'язання ($ billion)')
        plt.savefig(self.config.get_results_directory() + "/scatterplot_commitments.png")
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=self.df_allocations['Financial allocations($ billion)'],
                        y=self.df_allocations['Military allocations($ billion)'])
        plt.title('Діаграма розсіювання фінансових та військових асигнувань')
        plt.xlabel('Фінансові асигнування ($ billion)')
        plt.ylabel('Військові асигнування ($ billion)')
        plt.savefig(self.config.get_results_directory() + "/scatterplot_allocations.png")
        plt.show()

        print(f"\nГрафіки збережено у {self.config.get_results_directory()}.")

    def visualize_regression(self):
        """
        Візуалізує результати лінійної регресії за допомогою графіків.
        """

        # Для 'Financial Commitments.csv'
        # Побудова діаграми розсіювання з лінією регресії
        plt.figure(figsize=(10, 6))
        sns.regplot(x=self.test_commitments['Total bilateral commitments($ billion)'],
                    y=self.predictions_commitments,
                    scatter_kws={'s': 10}, line_kws={'color': 'red'})
        plt.title('Лінійна регресія для Financial Commitments')
        plt.xlabel('Фактичні значення (Total bilateral commitments, $ billion)')
        plt.ylabel('Прогнозовані значення')
        plt.savefig(self.config.get_results_directory() + "/regression_plot_commitments.png")
        plt.show()

        # Побудова графіка залишкових значень
        plt.figure(figsize=(10, 6))
        residuals_commitments = self.test_commitments['Total bilateral commitments($ billion)'] - self.predictions_commitments
        sns.scatterplot(x=self.predictions_commitments, y=residuals_commitments, s=10)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.title('Графік залишкових значень для Financial Commitments')
        plt.xlabel('Прогнозовані значення')
        plt.ylabel('Залишкові значення')
        plt.savefig(self.config.get_results_directory() + "/residuals_plot_commitments.png")
        plt.show()

        # Побудова графіка прогнозованих значень проти фактичних значень
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=self.test_commitments['Total bilateral commitments($ billion)'],
                        y=self.predictions_commitments, s=10)
        plt.plot([min(self.test_commitments['Total bilateral commitments($ billion)']), max(self.test_commitments['Total bilateral commitments($ billion)'])],
                 [min(self.test_commitments['Total bilateral commitments($ billion)']), max(self.test_commitments['Total bilateral commitments($ billion)'])],
                 color='red', linestyle='--')
        plt.title('Прогнозовані vs. Фактичні значення для Financial Commitments')
        plt.xlabel('Фактичні значення')
        plt.ylabel('Прогнозовані значення')
        plt.savefig(self.config.get_results_directory() + "/predicted_vs_actual_commitments.png")
        plt.show()

        # Для 'Financial Allocations.csv'
        # Побудова діаграми розсіювання з лінією регресії
        plt.figure(figsize=(10, 6))
        sns.regplot(x=self.test_allocations['Total bilateral allocations($ billion)'],
                    y=self.predictions_allocations,
                    scatter_kws={'s': 10}, line_kws={'color': 'red'})
        plt.title('Лінійна регресія для Financial Allocations')
        plt.xlabel('Фактичні значення (Total bilateral allocations, $ billion)')
        plt.ylabel('Прогнозовані значення')
        plt.savefig(self.config.get_results_directory() + "/regression_plot_allocations.png")
        plt.show()

        # Побудова графіка залишкових значень
        plt.figure(figsize=(10, 6))
        residuals_allocations = self.test_allocations['Total bilateral allocations($ billion)'] - self.predictions_allocations
        sns.scatterplot(x=self.predictions_allocations, y=residuals_allocations, s=10)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.title('Графік залишкових значень для Financial Allocations')
        plt.xlabel('Прогнозовані значення')
        plt.ylabel('Залишкові значення')
        plt.savefig(self.config.get_results_directory() + "/residuals_plot_allocations.png")
        plt.show()

        # Побудова графіка прогнозованих значень проти фактичних значень
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=self.test_allocations['Total bilateral allocations($ billion)'],
                        y=self.predictions_allocations, s=10)
        plt.plot([min(self.test_allocations['Total bilateral allocations($ billion)']), max(self.test_allocations['Total bilateral allocations($ billion)'])],
                 [min(self.test_allocations['Total bilateral allocations($ billion)']), max(self.test_allocations['Total bilateral allocations($ billion)'])],
                 color='red', linestyle='--')
        plt.title('Прогнозовані vs. Фактичні значення для Financial Allocations')
        plt.xlabel('Фактичні значення')
        plt.ylabel('Прогнозовані значення')
        plt.savefig(self.config.get_results_directory() + "/predicted_vs_actual_allocations.png")
        plt.show()

        print(f"\nГрафіки лінійної регресії збережено у {self.config.get_results_directory()}.")

    def build_model(self):
        """
        Будує модель лінійної регресії для прогнозування. Зберігає прогнози у файл.
        """
        # Лінійна регресія для 'Financial Commitments.csv'
        model_commitments = LinearRegression()
        X_train_commitments = self.train_commitments.drop('Total bilateral commitments($ billion)', axis=1)
        y_train_commitments = self.train_commitments['Total bilateral commitments($ billion)']
        X_test_commitments = self.test_commitments.drop('Total bilateral commitments($ billion)', axis=1)

        model_commitments.fit(X_train_commitments, y_train_commitments)
        self.predictions_commitments = model_commitments.predict(X_test_commitments) # Збереження прогнозів

        print("\nПрогнози для 'Financial Commitments.csv':")
        print(self.predictions_commitments)

        # Лінійна регресія для 'Financial Allocations.csv'
        model_allocations = LinearRegression()
        X_train_allocations = self.train_allocations.drop('Total bilateral allocations($ billion)', axis=1)
        y_train_allocations = self.train_allocations['Total bilateral allocations($ billion)']
        X_test_allocations = self.test_allocations.drop('Total bilateral allocations($ billion)', axis=1)
        
        model_allocations.fit(X_train_allocations, y_train_allocations)
        self.predictions_allocations = model_allocations.predict(X_test_allocations) # Збереження прогнозів

        print("\nПрогнози для 'Financial Allocations.csv':")
        print(self.predictions_allocations)

        # Зберігаємо прогнози у файл
        pd.DataFrame(self.predictions_commitments).to_csv(self.config.get_results_directory() + "/predictions_commitments.csv")
        pd.DataFrame(self.predictions_allocations).to_csv(self.config.get_results_directory() + "/predictions_allocations.csv")
        print(f"\nПрогнози збережено у {self.config.get_results_directory()}.")

    def analyze_dataset(self):
        """
        Виконує повний цикл аналізу даних.
        """
        self.load_data()
        self.preview_data()
        self.clean_data()
        self.transform_data()
        self.decompose_data()
        self.descriptive_statistics_and_visualization()
        self.build_model()
        self.visualize_regression()


if __name__ == "__main__":
    config = Config()
    analyzer = DatasetAnalyzer(config)
    analyzer.analyze_dataset()