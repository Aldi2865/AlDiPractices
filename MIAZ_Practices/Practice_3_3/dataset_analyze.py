import pandas as pd
import os
from config import Config
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(commitments_filepath, allocations_filepath):
    """
    Завантажує дані про фінансові зобов'язання та асигнування з двох CSV файлів.

    Args:
      commitments_filepath: Шлях до файлу 'Financial Commitments.csv'.
      allocations_filepath: Шлях до файлу 'Financial Allocations.csv'.

    Returns:
      Два pandas DataFrame: commitments_df та allocations_df,
      які містять дані з відповідних файлів.
      Повертає None, якщо файли не знайдені.
    """
    try:
        commitments_df = pd.read_csv(commitments_filepath)
        allocations_df = pd.read_csv(allocations_filepath)
        return commitments_df, allocations_df
    except FileNotFoundError:
        print(f"Помилка: Файли не знайдені. Перевірте шляхи:\n{commitments_filepath}\n{allocations_filepath}")
        return None, None

def analyze_data(commitments_df, allocations_df, output_dir):
    """
    Аналізує завантажені дані, будує графіки, зберігає результати в файл та графіки в окремі файли.

    Args:
        commitments_df: DataFrame з даними про зобов'язання.
        allocations_df: DataFrame з даними про асигнування.
        output_dir: Папка для збереження результатів.
    """
    print("Попередній аналіз даних:")

    # Перевірка на пропущені значення
    print("\nПропущені значення в 'Financial Commitments.csv':")
    print(commitments_df.isnull().sum())
    print("\nПропущені значення в 'Financial Allocations.csv':")
    print(allocations_df.isnull().sum())

    # Заповнення пропущених значень середнім значенням (закоментовано)
    # for column in commitments_df.columns:
    #     if commitments_df[column].isnull().any():
    #         if pd.api.types.is_numeric_dtype(commitments_df[column]):
    #             commitments_df[column].fillna(commitments_df[column].mean(), inplace=True)
    #         else:
    #             print(f"Пропуски в нечисловому стовпці '{column}' в 'Financial Commitments.csv' не замінено.")

    # for column in allocations_df.columns:
    #     if allocations_df[column].isnull().any():
    #         if pd.api.types.is_numeric_dtype(allocations_df[column]):
    #             allocations_df[column].fillna(allocations_df[column].mean(), inplace=True)
    #         else:
    #             print(f"Пропуски в нечисловому стовпці '{column}' в 'Financial Allocations.csv' не замінено.")

    # Видалення дублікатів
    commitments_df.drop_duplicates(inplace=True)
    allocations_df.drop_duplicates(inplace=True)

    # Перетворення категоріальних змінних на числові (якщо потрібно)
    if 'EU member' in commitments_df.columns:
        commitments_df['EU member'] = commitments_df['EU member'].map({1: 1, 0: 0})

    if 'EU member' in allocations_df.columns:
        allocations_df['EU member'] = allocations_df['EU member'].map({1: 1, 0: 0})

    # Об'єднуємо дані по країні
    merged_data = pd.merge(commitments_df, allocations_df, on="Country", suffixes=('_commitments', '_allocations'))

    # Відкриваємо файл для запису результатів
    with open(os.path.join(output_dir, "analysis_results.txt"), "w") as f:

        # Функція для запису результатів у файл та виведення на екран
        def print_and_write(message):
            print(message)
            f.write(str(message) + "\n")

        # Продовження аналізу після обробки даних
        print_and_write("\nЗагальна інформація про зобов'язання (після обробки):")
        print_and_write(commitments_df.info())

        print_and_write("\nЗагальна інформація про асигнування (після обробки):")
        print_and_write(allocations_df.info())

        print_and_write("\nОписова статистика для зобов'язань (після обробки):")
        print_and_write(commitments_df.describe())

        print_and_write("\nОписова статистика для асигнувань (після обробки):")
        print_and_write(allocations_df.describe())

        print_and_write("\nКількість країн-членів ЄС у даних про зобов'язання (після обробки):")
        print_and_write(commitments_df['EU member'].value_counts())

        print_and_write("\nКількість країн-членів ЄС у даних про асигнування (після обробки):")
        print_and_write(allocations_df['EU member'].value_counts())

        print_and_write("\nТоп 5 країн за загальними зобов'язаннями (після обробки):")
        print_and_write(commitments_df.sort_values(by="Total bilateral commitments($ billion)", ascending=False).head(5)[['Country', "Total bilateral commitments($ billion)"]])

        print_and_write("\nТоп 5 країн за загальними асигнуваннями (після обробки):")
        print_and_write(allocations_df.sort_values(by="Total bilateral allocations($ billion)", ascending=False).head(5)[['Country', "Total bilateral allocations($ billion)"]])

        print_and_write("\nСереднє співвідношення між виділеними коштами та зобов'язаннями для країн-членів ЄС (після обробки):")

        # Розрахунок співвідношення для всіх країн
        merged_data['Allocation_to_Commitment_Ratio'] = merged_data["Total bilateral allocations($ billion)"] / merged_data["Total bilateral commitments($ billion)"]

        # Виводимо середнє для ЄС
        eu_mean_ratio = merged_data[merged_data['EU member_commitments'] == 1]['Allocation_to_Commitment_Ratio'].mean()
        print_and_write(f"Середнє для країн ЄС: {eu_mean_ratio}")

        # Виводимо середнє для не-ЄС
        non_eu_mean_ratio = merged_data[merged_data['EU member_commitments'] == 0]['Allocation_to_Commitment_Ratio'].mean()
        print_and_write(f"Середнє для країн не-ЄС: {non_eu_mean_ratio}")

        # Замінюємо англійські назви колонок на українські для відображення на графіках
        merged_data = merged_data.rename(columns={
            'Total bilateral commitments($ billion)': 'Загальні двосторонні зобов\'язання ($ млрд)',
            'Total bilateral allocations($ billion)': 'Загальні двосторонні асигнування ($ млрд)',
            'EU member_commitments': 'Член ЄС (зобов\'язання)',
            'EU member_allocations': 'Член ЄС (асигнування)'
        })

        commitments_df = commitments_df.rename(columns={
            'Total bilateral commitments($ billion)': 'Загальні двосторонні зобов\'язання ($ млрд)'
        })

        allocations_df = allocations_df.rename(columns={
          'Total bilateral allocations($ billion)': 'Загальні двосторонні асигнування ($ млрд)'
        })

        # Візуалізація даних
        print_and_write("\nВізуалізація даних:")

        # Гістограма для 'Total bilateral commitments($ billion)'
        plt.figure(figsize=(10, 6))
        sns.histplot(commitments_df['Загальні двосторонні зобов\'язання ($ млрд)'], bins=20, kde=True)
        plt.title('Розподіл загальних двосторонніх зобов\'язань')
        plt.xlabel('Загальні двосторонні зобов\'язання ($ млрд)')
        plt.ylabel('Кількість країн')
        plt.savefig(os.path.join(output_dir, "histogram_commitments.png"))
        plt.show()

        # Гістограма для 'Total bilateral allocations($ billion)'
        plt.figure(figsize=(10, 6))
        sns.histplot(allocations_df['Загальні двосторонні асигнування ($ млрд)'], bins=20, kde=True)
        plt.title('Розподіл загальних двосторонніх асигнувань')
        plt.xlabel('Загальні двосторонні асигнування ($ млрд)')
        plt.ylabel('Кількість країн')
        plt.savefig(os.path.join(output_dir, "histogram_allocations.png"))
        plt.show()

        # Коробковий діаграма (boxplot) для 'Total bilateral commitments($ billion)' за групами 'EU member'
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='Член ЄС (зобов\'язання)', y='Загальні двосторонні зобов\'язання ($ млрд)', data=merged_data)
        plt.title('Загальні двосторонні зобов\'язання для країн-членів ЄС та інших країн')
        plt.xlabel('Член ЄС')
        plt.ylabel('Загальні двосторонні зобов\'язання ($ млрд)')
        plt.savefig(os.path.join(output_dir, "boxplot_commitments_eu.png"))
        plt.show()

        # Коробковий діаграма (boxplot) для 'Total bilateral allocations($ billion)' за групами 'EU member'
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='Член ЄС (асигнування)', y='Загальні двосторонні асигнування ($ млрд)', data=merged_data)
        plt.title('Загальні двосторонні асигнування для країн-членів ЄС та інших країн')
        plt.xlabel('Член ЄС')
        plt.ylabel('Загальні двосторонні асигнування ($ млрд)')
        plt.savefig(os.path.join(output_dir, "boxplot_allocations_eu.png"))
        plt.show()

        # Діаграма розсіювання для 'Total bilateral commitments($ billion)' vs 'Total bilateral allocations($ billion)'
        plt.figure(figsize=(10, 6))
        # Створюємо словник для заміни значень в легенді
        legend_dict = {1: "Так", 0: "Ні"}

        sns.scatterplot(x='Загальні двосторонні зобов\'язання ($ млрд)', y='Загальні двосторонні асигнування ($ млрд)',
                        data=merged_data, hue='Член ЄС (зобов\'язання)', palette={0: 'skyblue', 1: 'lightgreen'})

        plt.title('Залежність між загальними зобов\'язаннями та асигнуваннями')
        plt.xlabel('Загальні двосторонні зобов\'язання ($ млрд)')
        plt.ylabel('Загальні двосторонні асигнування ($ млрд)')

        # Отримуємо поточні мітки легенди
        handles, labels = plt.gca().get_legend_handles_labels()

        # Замінюємо мітки легенди, використовуючи словник
        plt.legend(handles=handles, labels=[legend_dict.get(int(label), label) for label in labels], title='Член ЄС')

        plt.savefig(os.path.join(output_dir, "scatterplot_commitments_allocations.png"))
        plt.show()

        # Кореляційна матриця
        plt.figure(figsize=(12, 10))
        sns.heatmap(commitments_df.corr(numeric_only=True), annot=True, cmap='coolwarm', annot_kws={"fontsize": 8})
        plt.title('Кореляційна матриця (Financial Commitments)')
        plt.xticks(fontsize=8, rotation=45, ha='right')
        plt.yticks(fontsize=8, rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_matrix_commitments.png"))
        plt.show()

        plt.figure(figsize=(12, 10))
        sns.heatmap(allocations_df.corr(numeric_only=True), annot=True, cmap='coolwarm', annot_kws={"fontsize": 8})
        plt.title('Кореляційна матриця (Financial Allocations)')
        plt.xticks(fontsize=8, rotation=45, ha='right')
        plt.yticks(fontsize=8, rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_matrix_allocations.png"))
        plt.show()

        # Створюємо груповані стовпчасті діаграми
        plt.figure(figsize=(14, 8))

        # Створюємо DataFrame для візуалізації
        plot_data = merged_data[['Country', 'Загальні двосторонні зобов\'язання ($ млрд)', 'Загальні двосторонні асигнування ($ млрд)', 'Член ЄС (зобов\'язання)']]
        plot_data = plot_data.melt(id_vars=['Country', 'Член ЄС (зобов\'язання)'], var_name='Type', value_name='Amount')

        # Замінюємо англійські назви на українські перед побудовою графіка
        plot_data['Type'] = plot_data['Type'].replace({
            'Загальні двосторонні зобов\'язання ($ млрд)': 'Загальні двосторонні зобов\'язання',
            'Загальні двосторонні асигнування ($ млрд)': 'Загальні двосторонні асигнування'
        })

        sns.barplot(x='Country', y='Amount', hue='Type', data=plot_data, palette=['skyblue', 'lightgreen'])

        # Додаємо легенду для 'EU member'
        for i, patch in enumerate(plt.gca().patches):
            if i < len(merged_data):
                if merged_data['Член ЄС (зобов\'язання)'].iloc[i] == 1:
                    patch.set_hatch('/')

        # показуємо легенду
        handles, labels = plt.gca().get_legend_handles_labels()
        handles.append(plt.Rectangle((0,0),1,1, fc="white",ec="black",hatch='/'))
        labels.append("Член ЄС")
        plt.legend(handles, labels, title='Тип / Членство в ЄС')

        plt.title('Порівняння зобов\'язань та асигнувань по країнах (з виділенням країн ЄС)')
        plt.xlabel('Країна')
        plt.ylabel('Сума ($ млрд)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "barplot_commitments_allocations.png"))
        plt.show()

if __name__ == "__main__":
    config = Config()

    commitments_file = os.path.join(config.get_dataset_directory(), "Financial Commitments.csv")
    allocations_file = os.path.join(config.get_dataset_directory(), "Financial Allocations.csv")
    output_directory = config.get_results_directory()

    commitments_df, allocations_df = load_data(commitments_file, allocations_file)

    if commitments_df is not None and allocations_df is not None:
        analyze_data(commitments_df, allocations_df, output_directory)