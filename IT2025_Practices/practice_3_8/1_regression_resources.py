# Завдання 1: Регресійна модель для прогнозу витрат ресурсів

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

print("--- Завдання 1: Регресійна модель для прогнозу витрат ресурсів ---")

# 1. Генеруємо штучний набір даних
# Припустимо, у нас є 8 характеристик, що впливають на витрати ресурсів
n_samples = 1000
n_features = 8
X = np.random.rand(n_samples, n_features) * 100 # Характеристики (напр., тривалість операції, кількість задіяних одиниць)
# Створюємо умовну формулу для розрахунку витрат + додаємо шум
weights = np.random.rand(n_features) * 5
y = X @ weights + np.random.randn(n_samples) * 15 # Цільова змінна - витрати ресурсів

print(f"Згенеровано {n_samples} прикладів з {n_features} ознаками.")

# 2. Розділення вибірки на тренувальну та тестову
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Розмір тренувальної вибірки: {X_train.shape}")
print(f"Розмір тестової вибірки: {X_test.shape}")

# 3. Масштабування даних (важливо для нейронних мереж)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Дані масштабовано за допомогою StandardScaler.")

# 4. Побудова моделі нейронної мережі для регресії
model_regression = Sequential([
    Dense(128, activation='relu', input_shape=(n_features,)), # Вхідний шар (кількість нейронів = кількість ознак)
    Dense(64, activation='relu'),                         # Прихований шар
    Dense(32, activation='relu'),                         # Ще один прихований шар
    Dense(1)                                              # Вихідний шар (1 нейрон, без активації для регресії)
])

model_regression.summary() # Виведемо архітектуру моделі

# 5. Компіляція моделі
# Оптимізатор 'adam' є хорошим вибором за замовчуванням.
# Функція втрат 'mse' (Mean Squared Error) є стандартною для регресії.
# Метрика 'mae' (Mean Absolute Error) дає більш інтерпретовану помилку.
model_regression.compile(optimizer='adam', loss='mse', metrics=['mae'])
print("Модель скомпільовано (optimizer='adam', loss='mse', metrics=['mae']).")

# 6. Навчання моделі
print("Починаємо навчання моделі...")
history_regression = model_regression.fit(
    X_train_scaled, y_train,
    epochs=100,           # Кількість епох навчання
    batch_size=32,        # Розмір пакету даних для одного кроку градієнта
    validation_split=0.2, # Використовуємо частину тренувальних даних для валідації на кожній епосі
    verbose=0             # verbose=0, щоб не виводити прогрес кожної епохи
)
print("Навчання завершено.")

# 7. Оцінка моделі на тестових даних
loss, mae = model_regression.evaluate(X_test_scaled, y_test, verbose=0)
print(f"\nОцінка моделі на тестових даних:")
print(f"Mean Squared Error (MSE): {loss:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")

# 8. Прогноз на тестових даних (опціонально)
# y_pred_regression = model_regression.predict(X_test_scaled)
# print("\nПриклад прогнозу для перших 5 тестових зразків:")
# for i in range(5):
#    print(f"Реальне значення: {y_test[i]:.2f}, Прогноз: {y_pred_regression[i][0]:.2f}")

print("-" * 60)