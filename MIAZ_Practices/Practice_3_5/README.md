# Аналіз фінансових зобов'язань та асигнувань для України (2021)

## Опис

Цей проект аналізує дані про фінансові, гуманітарні та військові зобов'язання та асигнування, зроблені різними країнами на користь України у 2021 році. Проект включає завантаження, очищення, трансформацію, візуалізацію даних та побудову моделі лінійної регресії для прогнозування загальних двосторонніх зобов'язань та асигнувань.

## Структура проекту

.
├── config.py          # Файл конфігурації (шляхи до файлів, параметри)
├── dataset_analyze.py # Основний файл з кодом для аналізу даних
├── DataSet             # Папка з файлами даних
│   ├── Financial Allocations.csv
│   └── Financial Commitments.csv
├──results            # Папка для збереження результатів аналізу (створюється автоматично)
│   ├── correlation_matrix_allocations.csv
│   ├── correlation_matrix_commitments.csv
│   ├── descriptive_statistics_allocations.csv
│   ├── descriptive_statistics_commitments.csv
│   ├── histogram_allocations.png
│   ├── histogram_commitments.png
│   ├── boxplot_allocations.png
│   ├── boxplot_commitments.png
│   ├── predicted_vs_actual_allocations.png
│   ├── predicted_vs_actual_commitments.png
│   ├── predictions_allocations.csv
│   ├── predictions_commitments.csv
│   ├── regression_plot_allocations.png
│   ├── regression_plot_commitments.png
│   ├── residuals_plot_allocations.png
│   ├── residuals_plot_commitments.png
│   ├── scatterplot_allocations.png
│   ├── scatterplot_commitments.png
│   ├── test_allocations.csv
│   ├── test_commitments.csv
│   ├── train_allocations.csv
│   ├── train_commitments.csv
│   ├── transformed_allocations.csv
│   └── transformed_commitments.csv
└── README.md          # Цей файл

## Файли даних

Проект використовує два файли даних у форматі CSV, розташовані в папці `DataSet`:

* **`Financial Commitments.csv`:** Містить інформацію про задекларовані зобов'язання країн.
* **`Financial Allocations.csv`:** Містить інформацію про фактично виділені кошти країнами.

### Опис колонок `Financial Commitments.csv`

| Колонка                                         | Опис                                                                                                                                                                                                                                                                                                                                              |
| :----------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Country                                                | Назва країни                                                                                                                                                                                                                                                                                                                               |
| EU member                                              | Чи є країна членом Європейського Союзу (1 - член ЄС, 0 - не член ЄС)                                                                                                                                                                                                                                   |
| GDP in 2021 ($ billion)                                | Валовий внутрішній продукт (ВВП) країни у 2021 році                                                                                                                                                                                                                                                             |
| Financial commitments ($ billion)                      | Задекларовані фінансові зобов'язання країни                                                                                                                                                                                                                                                                    |
| Humanitarian commitments ($ billion)                   | Задекларовані гуманітарні зобов'язання країни                                                                                                                                                                                                                                                                |
| Military commitments ($ billion)                       | Задекларовані військові зобов'язання країни                                                                                                                                                                                                                                                                    |
| Total bilateral commitments($ billion)                 | Загальна сума двосторонніх зобов'язань (фінансових, гуманітарних та військових), задекларованих країною, у мільярдах доларів. Це сума фінансових, гуманітарних та військових зобов'язань. |
| Share in EU commitments($ billion)                     | Частка країни у загальних зобов'язаннях ЄС у мільярдах доларів. Це показує, яку частину загальних зобов'язань ЄС з надання допомоги вносить ця країна.                                                                    |
| Specific weapons and equipment($ billion)              | Сума, виділена країною на конкретне озброєння та обладнання                                                                                                                                                                                                                                        |
| Financial commitments with military purpose($ billion) | Фінансові зобов'язання, спеціально призначені для військових цілей                                                                                                                                                                                                                          |
| Total bilateral commitments of short term($ billion)   | Загальна сума короткострокових двосторонніх зобов'язань, взятих країною                                                                                                                                                                                                                |

### Опис колонок `Financial Allocations.csv`

| Колонка                         | Опис                                                                                                                                                                                                                                                                                                                                |
| :------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Country                                | Назва країни                                                                                                                                                                                                                                                                                                                 |
| EU member                              | Чи є країна членом Європейського Союзу (1 - член ЄС, 0 - не член ЄС)                                                                                                                                                                                                                     |
| Financial allocations($ billion)       | Фактично виділена країною фінансова допомога                                                                                                                                                                                                                                                    |
| Humanitarian allocations($ billion)    | Фактично виділена країною гуманітарна допомога                                                                                                                                                                                                                                                |
| Military allocations($ billion)        | Фактично виділена країною військова допомога                                                                                                                                                                                                                                                    |
| Total bilateral allocations($ billion) | Загальна сума двосторонньої допомоги (фінансової, гуманітарної та військової), виділеної країною, у мільярдах доларів. Це сума фінансових, гуманітарних та військових асигнувань. |
| Share in EU allocations($ billion)     | Частка країни у загальних асигнуваннях ЄС у мільярдах доларів. Це показує, яку частину загальних асигнувань ЄС з надання допомоги вносить ця країна.                                                        |

## Встановлення та залежності

1. **Клонуйте репозиторій:**

   ```bash
   git clone <посилання на репозиторій>
   ```
2. **Встановіть необхідні бібліотеки:**

   ```bash
   pip install -r requirements.txt
   ```

   Файл `requirements.txt` (не показаний у структурі, але необхідний) повинен містити наступні бібліотеки:

   ```
   pandas
   scikit-learn
   seaborn
   matplotlib
   ```

## Використання

1. **Переконайтеся, що файли даних (`Financial Commitments.csv` та `Financial Allocations.csv`) знаходяться в папці `DataSet`.**
2. **Налаштуйте конфігурацію в `config.py` (за потреби).** Вкажіть правильні шляхи до папок з даними та результатами.
3. **Запустіть `dataset_analyze.py`:**

   ```bash
   python dataset_analyze.py
   ```

## Результати

Після виконання скрипт `dataset_analyze.py` згенерує наступні результати в папці `results`:

* **CSV файли:**

  * `transformed_commitments.csv`: Трансформовані дані (нормалізовані та з One-Hot Encoding) для `Financial Commitments.csv`.
  * `transformed_allocations.csv`: Трансформовані дані для `Financial Allocations.csv`.
  * `train_commitments.csv`: Навчальна вибірка для `Financial Commitments.csv`.
  * `test_commitments.csv`: Тестова вибірка для `Financial Commitments.csv`.
  * `train_allocations.csv`: Навчальна вибірка для `Financial Allocations.csv`.
  * `test_allocations.csv`: Тестова вибірка для `Financial Allocations.csv`.
  * `correlation_matrix_commitments.csv`: Кореляційна матриця для навчальної вибірки `Financial Commitments.csv`.
  * `correlation_matrix_allocations.csv`: Кореляційна матриця для навчальної вибірки `Financial Allocations.csv`.
  * `descriptive_statistics_commitments.csv`: Описова статистика для `Financial Commitments.csv`.
  * `descriptive_statistics_allocations.csv`: Описова статистика для `Financial Allocations.csv`.
  * `predictions_commitments.csv`: Прогнози моделі лінійної регресії для `Financial Commitments.csv`.
  * `predictions_allocations.csv`: Прогнози моделі лінійної регресії для `Financial Allocations.csv`.
* **PNG файли (графіки):**

  * Гістограми розподілу загальних двосторонніх зобов'язань та асигнувань.
  * Коробкові діаграми розподілу військових зобов'язань та асигнувань.
  * Діаграми розсіювання фінансових та військових зобов'язань/асигнувань.
  * Діаграми розсіювання з лінією регресії для обох моделей.
  * Графіки залишкових значень для обох моделей.
  * Графіки прогнозованих значень проти фактичних значень для обох моделей.

## Опис коду

* **`config.py`:** Містить клас `Config` для управління конфігураційними параметрами (шляхи до папок).
* **`dataset_analyze.py`:** Містить клас `DatasetAnalyzer`, який виконує аналіз даних.

### `DatasetAnalyzer`

* **`__init__(self, config)`:** Конструктор класу.
* **`load_data(self)`:** Завантажує дані з CSV файлів.
* **`preview_data(self)`:** Виводить перші рядки та інформацію про дані.
* **`clean_data(self)`:** Очищує дані (заповнює пропущені значення нулями, видаляє дублікати).
* **`transform_data(self)`:** Трансформує дані (нормалізує числові, One-Hot Encoding для категоріальних).
* **`decompose_data(self)`:** Розділяє дані на навчальну та тестову вибірки, обчислює кореляційну матрицю.
* **`descriptive_statistics_and_visualization(self)`:** Обчислює описову статистику та будує графіки.
* **`build_model(self)`:** Будує моделі лінійної регресії, робить прогнози.
* **`visualize_regression(self)`:** Візуалізує результати лінійної регресії.
* **`analyze_dataset(self)`:** Виконує повний цикл аналізу даних.

## Автор

Al Di
