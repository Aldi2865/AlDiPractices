import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler # Додано для масштабування даних

# --- 1. Налаштування та Генерація даних ---

# Встановлення random seed для відтворюваності
np.random.seed(42)
tf.random.set_seed(42)

# Генерація синтетичних даних для класифікації
# n_samples: кількість зразків
# n_features: кількість ознак (вхідних даних для мережі)
# n_classes: кількість класів для класифікації
# n_informative: кількість інформативних ознак
# n_redundant: кількість надлишкових ознак (лінійні комбінації інформативних)
# random_state: для відтворюваності генерації
n_features = 20
n_classes = 3
n_samples=10000
X, y = make_classification(n_samples=n_samples,
                           n_features=n_features,
                           n_informative=10,
                           n_redundant=5,
                           n_classes=n_classes,
                           random_state=42)

print(f"Форма даних X: {X.shape}") # (2000, 20)
print(f"Форма міток y: {y.shape}")   # (2000,)
print(f"Унікальні класи: {np.unique(y)}") # [0 1 2]

# --- 2. Підготовка даних ---

# Розділення даних на тренувальний та тестовий набори (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) # stratify=y зберігає пропорції класів

# Масштабування даних (дуже важливо для нейронних мереж)
# MLP чутливі до масштабу вхідних даних
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test) # Використовуємо scaler, навчений на тренувальних даних

print(f"Форма X_train: {X_train.shape}, Форма y_train: {y_train.shape}")
print(f"Форма X_test: {X_test.shape}, Форма y_test: {y_test.shape}")

# --- 3. Побудова моделі MLP ---

model = Sequential(name="Simple_MLP")

# Вхідний шар неявно визначається через input_shape у першому Dense шарі
# Перший прихований шар: 64 нейрони, функція активації ReLU
model.add(Dense(64, activation='relu', input_shape=(n_features,), name="Hidden_Layer_1"))

# Другий прихований шар: 32 нейрони, функція активації ReLU
model.add(Dense(32, activation='relu', name="Hidden_Layer_2"))

# Вихідний шар: кількість нейронів = кількість класів (n_classes)
# Функція активації 'softmax' для багатокласової класифікації (видає ймовірності для кожного класу)
model.add(Dense(n_classes, activation='softmax', name="Output_Layer"))

# --- 4. Компіляція моделі ---

# Оптимізатор: 'adam' - популярний та ефективний вибір
# Функція втрат: 'sparse_categorical_crossentropy' - підходить, коли мітки класів (y) є цілими числами (0, 1, 2...).
# Якщо б мітки були у форматі one-hot encoding (напр., [1,0,0], [0,1,0]), використовували б 'categorical_crossentropy'.
# Метрики: 'accuracy' - відсоток правильно класифікованих зразків
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Виведення структури моделі
model.summary()

# --- 5. Навчання моделі ---

epochs = 50 # Кількість епох навчання
batch_size = 32 # Розмір міні-пакета даних на кожній ітерації

print("\nПочаток навчання моделі...")
# validation_data дозволяє відстежувати продуктивність на тестовому наборі після кожної епохи
history = model.fit(X_train, y_train,
                    epochs=epochs,
                    batch_size=batch_size,
                    validation_data=(X_test, y_test),
                    verbose=1) # verbose=1 показує прогрес навчання

# --- 6. Оцінка моделі ---

print("\nОцінка моделі на тестових даних:")
loss, accuracy = model.evaluate(X_test, y_test, verbose=0) # verbose=0 приховує виведення під час оцінки

print(f"Втрати моделі на тесті (Test Loss): {loss:.4f}")
print(f"Точність моделі на тесті (Test Accuracy): {accuracy:.4f}")

# --- 7. Візуалізація процесу навчання ---

# Отримуємо