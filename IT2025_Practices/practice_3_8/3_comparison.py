# Завдання 3 (Виправлено): Порівняння функцій активації ('relu' vs 'tanh') на прикладі регресії

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import time # Для вимірювання часу навчання

print("\n--- Завдання 3 (Виправлено): Порівняння функцій активації ('relu' vs 'tanh') ---")

# --- Початок блоку підготовки даних (залишено для самодостатності) ---
# Переконуємось, що дані існують або генеруємо їх
try:
    # Спробуємо використати дані, якщо вони залишились з Завдання 1
    X_train_scaled.shape
    print("Використання даних, підготовлених у попередніх завданнях.")
except NameError:
    print("Попередні дані не знайдено. Генеруємо та готуємо дані для Завдання 3...")
    n_samples = 1000
    n_features = 8
    X = np.random.rand(n_samples, n_features) * 100
    weights = np.random.rand(n_features) * 5
    y = X @ weights + np.random.randn(n_samples) * 15
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("Дані згенеровано та підготовлено.")
# --- Кінець блоку підготовки даних ---


# --- Модель 1: З активацією 'relu' ---
print("\nСтворення та навчання моделі з 'relu'...")
model_relu = Sequential([
    Dense(128, activation='relu', input_shape=(n_features,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)
])
model_relu.compile(optimizer='adam', loss='mse', metrics=['mae'])
# model_relu.summary() # Можна розкоментувати, щоб побачити архітектуру

start_time = time.time()
history_relu = model_relu.fit(
    X_train_scaled, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=0 # Не виводити прогрес
)
relu_train_time = time.time() - start_time
print(f"Модель 'relu' навчено за {relu_train_time:.2f} сек.")

# Оцінка моделі 'relu'
loss_relu, mae_relu = model_relu.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Оцінка 'relu': MSE={loss_relu:.2f}, MAE={mae_relu:.2f}")


# --- Модель 2: З активацією 'tanh' ---
print("\nСтворення та навчання моделі з 'tanh'...")
model_tanh = Sequential([
    Dense(128, activation='tanh', input_shape=(n_features,)), # Замінено 'relu' на 'tanh'
    Dense(64, activation='tanh'),                         # Замінено 'relu' на 'tanh'
    Dense(32, activation='tanh'),                         # Замінено 'relu' на 'tanh'
    Dense(1)                                              # Вихідний шар без змін
])
model_tanh.compile(optimizer='adam', loss='mse', metrics=['mae']) # Ті ж параметри компіляції
# model_tanh.summary() # Можна розкоментувати

start_time = time.time()
history_tanh = model_tanh.fit(
    X_train_scaled, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=0 # Не виводити прогрес
)
tanh_train_time = time.time() - start_time
print(f"Модель 'tanh' навчено за {tanh_train_time:.2f} сек.")

# Оцінка моделі 'tanh'
loss_tanh, mae_tanh = model_tanh.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Оцінка 'tanh': MSE={loss_tanh:.2f}, MAE={mae_tanh:.2f}")


# --- Порівняння результатів ---
print("\n--- Порівняння результатів (ReLU vs Tanh) ---")
print(f"                     |   ReLU   |   Tanh   |")
print(f"---------------------|----------|----------|")
print(f"MSE (Test Loss)      | {loss_relu:^8.2f} | {loss_tanh:^8.2f} |")
print(f"MAE (Test Metric)    | {mae_relu:^8.2f} | {mae_tanh:^8.2f} |")
print(f"Час навчання (сек)   | {relu_train_time:^8.2f} | {tanh_train_time:^8.2f} |")
print("-" * 60)

# Короткий висновок (може варіюватися залежно від даних та запуску)
print("\nВисновки:")
if loss_relu < loss_tanh:
    print("- На цих даних модель з 'relu' показала кращі результати за метрикою MSE.")
elif loss_tanh < loss_relu:
     print("- На цих даних модель з 'tanh' показала кращі результати за метрикою MSE.")
else:
     print("- На цих даних моделі показали схожі результати за метрикою MSE.")

print("- 'relu' часто навчається швидше і може бути менш схильною до проблеми зникаючого градієнта.")
print("- 'tanh' обмежує вихідні значення шару між -1 та 1.")
print("- Вибір функції активації залежить від конкретної задачі та даних.")
print("-" * 60)