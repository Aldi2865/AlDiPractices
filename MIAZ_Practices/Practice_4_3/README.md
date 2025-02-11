# Аналіз даних та побудова моделей регресії

Цей репозиторій містить Jupyter Notebook з аналізом даних та побудовою моделей регресії для прогнозування фінансових показників.

## Опис файлів

* `steps.ipynb`: Jupyter Notebook з покроковим аналізом даних, візуалізацією та моделюванням.
* `report.ipynb`: Jupyter Notebook з коротким звітом, що містить опис використаного підходу, ключові результати, графіки та висновки.
* `DataSet/financial_regression.csv`: Набір даних, що містить фінансові показники.

## Кроки аналізу

1. **Попередня обробка даних:**

   * Завантаження даних.
   * Перевірка на наявність пропущених значень та їх обробка.
   * Перетворення дати в числові ознаки (рік, місяць, день тижня, день місяця).
2. **Аналіз даних:**

   * Побудова кореляційної матриці.
3. **Розподіл даних:**

   * Розділення даних на тренувальний та тестовий набори (80:20).
4. **Побудова та оцінка моделей:**

   * Навчання базової моделі лінійної регресії.
   * Навчання та порівняння моделей Ridge, Lasso та Decision Tree регресії.
   * Оцінка якості моделей за допомогою метрик R^2 та MSE.
5. **Відбір ознак:**

   * Застосування методів відбору ознак на основі кореляції (фільтр) та з використанням Lasso (вбудований метод).
   * Навчання моделей лінійної регресії на відібраних ознаках та порівняння результатів.
6. **Оптимізація гіперпараметрів:**

   * Використання Grid Search для підбору оптимальних гіперпараметрів для моделей Ridge, Lasso та Decision Tree.
   * Навчання моделей з оптимальними гіперпараметрами та порівняння результатів.
7. **Оформлення звіту:**

   * Підготовка короткого звіту з описом використаного підходу, ключових результатів, графіків та висновків (файл `report.ipynb`).

## Використані бібліотеки

* `pandas`
* `numpy`
* `matplotlib`
* `seaborn`
* `sklearn`

## Встановлення

Для запуску коду необхідно встановити перелічені вище бібліотеки. Це можна зробити за допомогою `pip`:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```
