import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.callbacks import EarlyStopping

# --- 1. Генерація Синтетичних Даних ---
# (Для реальних даних цей блок замінюється на завантаження та очищення даних)

np.random.seed(42)
tf.random.set_seed(42)

# Параметри часового ряду
n_points = 1500  # Загальна кількість точок даних
noise_level = 0.05 # Рівень шуму
trend_factor = 0.001 # Невеликий тренд
period1 = 50     # Періодичність першої синусоїди
period2 = 100    # Періодичність другої синусоїди

# Створення часового ряду
time = np.arange(n_points)
# Комбінація синусоїд, тренду та шуму
data = 10 * np.sin(2 * np.pi * time / period1) + \
       5 * np.sin(2 * np.pi * time / period2) + \
       trend_factor * time**1.5 + \
       noise_level * np.random.randn(n_points) * 30 + 100 # Додаємо базове значення

# Перетворюємо у формат (n_points, 1) для зручності масштабування
data = data.reshape(-1, 1)

print(f"Згенеровано {n_points} точок даних.")
plt.figure(figsize=(12, 4))
plt.plot(time, data)
plt.title("Синтетичний часовий ряд (імітація курсу)")
plt.xlabel("Час")
plt.ylabel("Значення")
plt.grid(True)
plt.show()

# --- 2. Підготовка Даних ---

# Масштабування даних у діапазон [0, 1] (поширений підхід для LSTM)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Функція для створення послідовностей (вікон)
def create_sequences(data, n_steps):
    X, y = [], []
    for i in range(len(data) - n_steps):
        # Вхідна послідовність (вікно)
        X.append(data[i:(i + n_steps), 0])
        # Вихідне значення (наступна точка після вікна)
        y.append(data[i + n_steps, 0])
    return np.array(X), np.array(y)

# Параметри послідовності
n_steps = 60  # Використовуємо попередні 60 днів для прогнозу наступного

# Створення послідовностей
X, y = create_sequences(scaled_data, n_steps)

# Розділення на тренувальний та тестовий набори (хронологічно!)
split_ratio = 0.8
split_index = int(len(X) * split_ratio)

X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

# Зміна форми X для входу в LSTM: [зразки, кроки_часу, ознаки]
# У нас одна ознака (сам курс)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

print(f"\nФорма X_train: {X_train.shape}") # (~1152, 60, 1)
print(f"Форма y_train: {y_train.shape}") # (~1152,)
print(f"Форма X_test: {X_test.shape}")  # (~288, 60, 1)
print(f"Форма y_test: {y_test.shape}")  # (~288,)


# --- 3. Побудова LSTM Моделі ---

model = Sequential(name="LSTM_TimeSeries_Forecast")
# Перший LSTM шар. units=50 - кількість нейронів у шарі.
# return_sequences=True, якщо наступний шар також LSTM.
# input_shape=(n_steps, 1) - (довжина послідовності, кількість ознак)
model.add(LSTM(units=50, return_sequences=True, input_shape=(n_steps, 1)))
model.add(Dropout(0.2)) # Dropout для регуляризації

# Другий LSTM шар
model.add(LSTM(units=50, return_sequences=False)) # False, бо далі йде Dense шар
model.add(Dropout(0.2))

# Вихідний шар: 1 нейрон для прогнозу одного значення.
# Активація лінійна (за замовчуванням для Dense), оскільки це регресія.
model.add(Dense(units=1))


# --- 4. Компіляція та Навчання Моделі ---

# Оптимізатор Adam - хороший вибір для початку
# Функція втрат 'mean_squared_error' (MSE) - стандарт для регресії
# Метрика 'mae' (Mean Absolute Error) - для інтерпретації помилки у вихідних одиницях
print("\nКомпіляція моделі...")
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

model.summary()

# Рання зупинка для запобігання перенавчанню
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

print("\nПочаток навчання моделі...")
history = model.fit(X_train, y_train,
                    epochs=100, # Максимальна кількість епох
                    batch_size=32,
                    validation_data=(X_test, y_test),
                    callbacks=[early_stopping],
                    verbose=1)


# --- 5. Прогнозування на Тестових Даних ---

print("\nСтворення прогнозів на тестових даних...")
predicted_scaled = model.predict(X_test)

# --- 6. Оцінка Моделі ---

# Повернення даних до оригінального масштабу для оцінки та візуалізації
predicted_original = scaler.inverse_transform(predicted_scaled)
y_test_original = scaler.inverse_transform(y_test.reshape(-1, 1))

# Розрахунок метрик регресії
rmse = np.sqrt(mean_squared_error(y_test_original, predicted_original))
mae = mean_absolute_error(y_test_original, predicted_original)

print("\nОцінка моделі на тестових даних (в оригінальному масштабі):")
print(f"  Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"  Mean Absolute Error (MAE):    {mae:.4f}")

# Додатково: Оцінка MAE у відсотках від середнього значення
mean_value = np.mean(y_test_original)
mape_like = (mae / mean_value) * 100
print(f"  Mean Absolute Percentage Error (MAPE-like): {mape_like:.2f}%")


# --- 7. Візуалізація Результатів ---

print("\nВізуалізація прогнозів...")

plt.figure(figsize=(14, 6))
plt.plot(y_test_original, color='blue', label='Справжні значення (Actual)')
plt.plot(predicted_original, color='red', linestyle='--', label='Прогнозовані значення (Predicted)')
plt.title('Прогноз часового ряду за допомогою LSTM')
plt.xlabel('Час (тестовий період)')
plt.ylabel('Значення курсу (оригінальний масштаб)')
plt.legend()
plt.grid(True)
plt.show()

# Графік втрат під час навчання
plt.figure(figsize=(10, 4))
plt.plot(history.history['loss'], label='Втрати на тренуванні (Training Loss)')
plt.plot(history.history['val_loss'], label='Втрати на валідації (Validation Loss)')
plt.title('Динаміка втрат під час навчання')
plt.xlabel('Епохи')
plt.ylabel('MSE Loss')
plt.legend()
plt.grid(True)
plt.show()

print("EXECUTION COMPLETED.")
# --- Кінець коду ---