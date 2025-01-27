import tensorflow as tf  # Імпортуємо бібліотеку TensorFlow для роботи з нейронними мережами
from tensorflow import keras  # Імпортуємо Keras, високорівневий API для TensorFlow
from sklearn.datasets import make_regression, make_classification  # Імпортуємо функції для генерації даних
from sklearn.model_selection import train_test_split  # Імпортуємо функцію для розділення даних на тренувальні та тестові
import matplotlib.pyplot as plt  # Імпортуємо бібліотеку для візуалізації даних
import numpy as np  # Імпортуємо бібліотеку NumPy для роботи з масивами
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix  # Імпортуємо метрики для оцінки моделей
import seaborn as sns  # Імпортуємо бібліотеку Seaborn для візуалізації матриці плутанини

student_id = 3  # Мій номер а журналом

# 1. Генерація даних

# --- Регресія ---
X_reg, y_reg = make_regression(
    n_samples=1000 * student_id,  # Кількість зразків даних (1000 помножено на номер за журналом)
    n_features=1,  # Кількість ознак (вхідних змінних) для кожного зразка (в даному випадку 1)
    noise=10,  # Стандартне відхилення Гаусівського шуму, доданого до вихідних даних
    # --- інші параметри ---
    # bias=0.0,  # Зсув лінії регресії
    # coef=False,  # Чи повертати коефіцієнти регресії (True/False)
    # effective_rank=None,  # Ефективний ранг матриці ознак
    # tail_strength=0.5,  # Сила "хвостів" розподілу помилок
    # random_state=None  # Фіксоване значення для генератора випадкових чисел
)  

# --- Класифікація ---
X_class, y_class = make_classification(
    n_samples=1000 * student_id,  # Кількість зразків даних (1000 помножено на номер за журналом)
    n_features=4,  # Кількість ознак (вхідних змінних) для кожного зразка (в даному випадку 4)
    n_informative=4,  # Кількість інформативних ознак, які фактично використовуються для генерації даних
    n_redundant=0,  # Кількість надлишкових ознак, які є лінійними комбінаціями інформативних ознак
    n_repeated=0,  # Кількість повторюваних ознак, які є дублікатами інформативних або надлишкових ознак
    n_classes=student_id + 2,  # Кількість класів (номер за журналом + 2)
    n_clusters_per_class=1,  # Кількість кластерів на клас
    flip_y=0.01,  # Відсоток міток, які будуть випадково змінені
    class_sep=1.0,  # Відстань між кластерами
    random_state=42  # Фіксоване значення для генератора випадкових чисел
    # weights=None,  # Список ваг для кожного класу (None - рівні ваги) - значення за замовчуванням
    # hypercube=True,  # Чи генерувати дані в гіперкубі - значення за замовчуванням
    # shift=0.0,  # Зсув даних - значення за замовчуванням
    # scale=1.0,  # Масштабування даних - значення за замовчуванням
    # shuffle=True,  # Чи перемішувати дані - значення за замовчуванням
)

# --- Візуалізація ---
plt.figure(figsize=(12, 5))  # Створюємо фігуру для графіків розміром 12x5 дюймів

plt.subplot(1, 2, 1)  # Створюємо перший підграфік (1 рядок, 2 стовпці, 1-й графік)
plt.scatter(
    X_reg,  # Дані для осі X
    y_reg,  # Дані для осі Y
    s=10,  # Розмір точок
    c='blue',  # Колір точок
    marker='o',  # Форма маркерів (точки)
    alpha=0.5  # Прозорість точок
)  
plt.title('Дані для регресії')  # Додаємо заголовок
plt.xlabel('X')  # Додаємо підпис осі X
plt.ylabel('y')  # Додаємо підпис осі Y

plt.subplot(1, 2, 2)  # Створюємо другий підграфік (1 рядок, 2 стовпці, 2-й графік)
plt.scatter(
    X_class[:, 0],  # Дані для осі X (перша ознака)
    X_class[:, 1],  # Дані для осі Y (друга ознака)
    c=y_class,  # Колір точок залежить від класу
    s=10,  # Розмір точок
    cmap='viridis',  # Кольорова шкала
    marker='o',  # Форма маркерів (точки)
    alpha=0.5  # Прозорість точок
)  
plt.title('Дані для класифікації')  # Додаємо заголовок
plt.xlabel('X1')  # Додаємо підпис осі X
plt.ylabel('X2')  # Додаємо підпис осі Y

plt.show()  # Відображаємо графіки

# 2. Побудова та навчання моделей

# --- Регресія ---
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(  # Розділяємо дані на тренувальні та тестові
    X_reg,  # Вхідні дані
    y_reg,  # Вихідні дані
    test_size=0.2,  # Розмір тестової вибірки (20%)
    train_size=None,  # Розмір тренувальної вибірки (None - автоматично)
    random_state=42,  # Фіксоване значення для генератора випадкових чисел
    shuffle=True,  # Чи перемішувати дані перед розділенням
    stratify=None  # Розподіл класів (для класифікації)
)  

model_reg = keras.Sequential([  # Створюємо послідовну модель
    keras.layers.Dense(
        64,  # Кількість нейронів у шарі
        activation='relu',  # Функція активації - ReLU
        input_shape=(X_train_reg.shape[1],),  # Розмірність вхідних даних
        # --- інші параметри ---
        # use_bias=True,  # Чи використовувати зсув
        # kernel_initializer='glorot_uniform',  # Ініціалізація ваг
        # bias_initializer='zeros',  # Ініціалізація зсувів
        # kernel_regularizer=None,  # Регуляризація ваг
        # bias_regularizer=None,  # Регуляризація зсувів
        # activity_regularizer=None,  # Регуляризація активацій
        # kernel_constraint=None,  # Обмеження на ваги
        # bias_constraint=None  # Обмеження на зсуви
    ),  
    keras.layers.Dense(32, activation='relu'),  # Другий шар з 32 нейронами, функція активації ReLU
    keras.layers.Dense(1)  # Вихідний шар з 1 нейроном (для регресії)
])

model_reg.compile(
    loss='mse',  # Функція втрат - середня квадратична помилка (Mean Squared Error)
    optimizer='adam',  # Оптимізатор - Adam
    # --- інші параметри ---
    # metrics=None,  # Список метрик для оцінки
    # loss_weights=None,  # Ваги для різних виходів (якщо їх декілька)
    # weighted_metrics=None,  # Ваги для різних метрик
    # run_eagerly=None,  # Чи виконувати операції відразу
    # steps_per_execution=None  # Кількість кроків за одне виконання
)  


model_reg.fit(
    X_train_reg,  # Тренувальні вхідні дані
    y_train_reg,  # Тренувальні вихідні дані
    batch_size=None,  # Розмір пакету даних (None - весь набір)
    epochs=100,  # Кількість епох навчання
    verbose=0,  # 0 - приховати інформацію про процес навчання, 1 - показувати прогрес, 2 - показувати лише епохи
    callbacks=None,  # Список функцій зворотного виклику
    validation_split=0.0,  # Частина тренувальних даних для валідації
    validation_data=None,  # Дані для валідації
    shuffle=True,  # Чи перемішувати дані перед кожною епохою
    class_weight=None,  # Ваги для різних класів (для класифікації)
    sample_weight=None,  # Ваги для різних зразків
    initial_epoch=0,  # Початкова епоха
    steps_per_epoch=None,  # Кількість кроків за епоху
    validation_steps=None,  # Кількість кроків валідації
    validation_batch_size=None,  # Розмір пакету даних для валідації
    validation_freq=1,  # Частота валідації (кожні N епох)
    #max_queue_size=10,   Максимальний розмір черги даних
    #workers=1,   Кількість процесів для завантаження даних
    #use_multiprocessing=False   Чи використовувати багатопроцесорність
)  

# --- Класифікація ---
X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(  # Розділяємо дані на тренувальні та тестові
    X_class, y_class, test_size=0.2, random_state=42
)

model_class = keras.Sequential([  # Створюємо послідовну модель
    keras.layers.Dense(64, activation='relu', input_shape=(X_train_class.shape[1],)),  # Перший шар з 64 нейронами, функція активації ReLU
    keras.layers.Dense(32, activation='relu'),  # Другий шар з 32 нейронами, функція активації ReLU
    keras.layers.Dense(student_id + 2, activation='softmax')  
    # Вихідний шар з кількістю нейронів, що дорівнює кількості класів, функція активації softmax (для класифікації)
])

model_class.compile(
    loss='sparse_categorical_crossentropy',  # Функція втрат для класифікації з цілочисельними мітками класів
    optimizer='adam',  # Оптимізатор - Adam
    metrics=['accuracy']  # Метрика для оцінки - точність (accuracy)
)  

model_class.fit(
    X_train_class,  # Тренувальні вхідні дані
    y_train_class,  # Тренувальні вихідні дані
    epochs=100,  # Кількість епох навчання
    verbose=1  # 0 - приховати інформацію про процес навчання
)  

# 3. Оцінка моделей

# --- Регресія ---
y_pred_reg = model_reg.predict(X_test_reg)  # Робимо передбачення на тестових даних
mse = mean_squared_error(
    y_test_reg,  # Справжні значення
    y_pred_reg,  # Передбачені значення
    # --- інші параметри ---
    # sample_weight=None,  # Ваги для різних зразків
    # multioutput='uniform_average'  # Як обробляти багатовимірні вихідні дані
)  
print(f'Mean Squared Error (Регресія): {mse}')  # Виводимо результат

# --- Класифікація ---
y_pred_class = np.argmax(
    model_class.predict(X_test_class),  # Передбачені ймовірності для кожного класу
    axis=1  # Вісь, по якій визначається клас з найбільшою ймовірністю
)  
accuracy = accuracy_score(y_test_class, y_pred_class)  # Обчислюємо точність
print(f'Accuracy (Класифікація): {accuracy}')  # Виводимо результат

cm = confusion_matrix(
    y_test_class,  # Справжні мітки класів
    y_pred_class,  # Передбачені мітки класів
    # --- інші параметри ---
    # labels=None,  # Список міток класів
    # sample_weight=None,  # Ваги для різних зразків
    # normalize=None  # Нормалізація матриці (None, 'true', 'pred', 'all')
)  
plt.figure(figsize=(8, 6))  # Створюємо фігуру для графіка розміром 8x6 дюймів
sns.heatmap(
    cm,  # Матриця плутанини
    annot=True,  # Показувати значення в комірках
    fmt='d',  # Формат значень (цілі числа)
    cmap='Blues',  # Кольорова шкала
    # --- інші параметри ---
    # linewidths=0,  # Ширина ліній між комірками
    # linecolor='white',  # Колір ліній між комірками
    # cbar=True,  # Показувати кольорову шкалу
    # square=False,  # Чи робити комірки квадратними
    # xticklabels='auto',  # Мітки для осі X
    # yticklabels='auto',  # Мітки для осі Y
    # mask=None  # Маска для приховування деяких комірок
)  
plt.title('Матриця плутанини')  # Додаємо заголовок
plt.xlabel('Передбачені класи')  # Додаємо підпис осі X
plt.ylabel('Справжні класи')  # Додаємо підпис осі Y
plt.show()  # Відображаємо графік

# 4. Висновки

# Додайте сюди свої висновки щодо роботи моделей, 
# враховуючи метрики оцінки та візуалізацію даних.
# Наприклад, як впливає кількість нейронів, кількість шарів, 
# функції активації, оптимізатори на результати.