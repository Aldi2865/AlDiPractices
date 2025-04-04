import numpy as np
import pandas as pd # Використовуємо Pandas для зручної роботи з даними
import matplotlib.pyplot as plt
import requests # Для запитів до API
import json
from datetime import date, timedelta

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.callbacks import EarlyStopping

# --- 1. Завантаження Даних з API НБУ ---

np.random.seed(42)
tf.random.set_seed(42)

# Визначення періоду для завантаження даних
# NBU API може мати обмеження, почнемо з кількох останніх років
end_date = date.today()
# Наприклад, завантажимо дані за останні ~4 роки (враховуйте можливі зміни в API)
start_date = end_date - timedelta(days=4*365)

# Форматування дат для URL API
start_date_str = start_date.strftime('%Y%m%d')
end_date_str = end_date.strftime('%Y%m%d')
valcode = 'USD' # Код валюти долара США

# URL для отримання даних за період (перевірено станом на квітень 2025, може змінитися)
api_url = f"https://bank.gov.ua/NBU_Exchange/exchange_site?start={start_date_str}&end={end_date_str}&valcode={valcode}&sort=exchangedate&order=asc&json"

print(f"Завантаження даних курсу {valcode} з API НБУ за період {start_date} - {end_date}...")
print(f"URL запиту: {api_url}")

try:
    response = requests.get(api_url)
    response.raise_for_status() # Перевірка на HTTP помилки (4xx, 5xx)
    raw_data = response.json()
    print("Дані успішно завантажено.")

    # Перетворення JSON у Pandas DataFrame
    df = pd.DataFrame(raw_data)

    # Перевірка наявності даних
    if df.empty:
        raise ValueError("API НБУ повернуло порожній результат. Перевірте період або код валюти.")

    print(f"Отримано {len(df)} записів.")
    # print("Перші 5 записів:")
    # print(df.head())

except requests.exceptions.RequestException as e:
    print(f"Помилка запиту до API НБУ: {e}")
    # У разі помилки можна спробувати завантажити з локального файлу або зупинити скрипт
    exit()
except json.JSONDecodeError:
    print("Помилка розбору JSON відповіді від API НБУ.")
    exit()
except ValueError as e:
    print(e)
    exit()


# --- 2. Обробка та Підготовка Даних ---

# Вибираємо потрібні колонки і перейменовуємо для зручності
df = df[['exchangedate', 'rate']]
df.rename(columns={'exchangedate': 'Date', 'rate': 'Rate'}, inplace=True)

# Перетворюємо колонку 'Date' у формат datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

# Встановлюємо дату як індекс
df.set_index('Date', inplace=True)

# Сортуємо за датою (хоча API вже має сортувати)
df.sort_index(inplace=True)

# Перевірка на пропуски (хоча для офіційних курсів їх зазвичай немає)
if df['Rate'].isnull().any():
    print("Знайдено пропуски в даних! Заповнення за допомогою ffill...")
    df['Rate'].fillna(method='ffill', inplace=True) # Заповнюємо пропуски попереднім значенням

# --- Можливий крок: Візуалізація завантажених даних ---
plt.figure(figsize=(14, 5))
plt.plot(df.index, df['Rate'])
plt.title(f"Офіційний курс {valcode}/UAH НБУ ({start_date} - {end_date})")
plt.xlabel("Дата")
plt.ylabel("Курс")
plt.grid(True)
plt.show()

# Беремо тільки значення курсу для моделі
data = df['Rate'].values.reshape(-1, 1)

# Масштабування даних
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Функція для створення послідовностей (та ж сама)
def create_sequences(data, n_steps):
    X, y = [], []
    for i in range(len(data) - n_steps):
        X.append(data[i:(i + n_steps), 0])
        y.append(data[i + n_steps, 0])
    return np.array(X), np.array(y)

# Параметри послідовності (можна експериментувати)
n_steps = 30 # Використовуємо дані за попередні 30 днів

X, y = create_sequences(scaled_data, n_steps)

# Розділення на тренувальний та тестовий набори (хронологічно!)
# Враховуючи специфіку курсу, можна взяти менший тестовий період, напр. останні 6 міс або рік
split_ratio = 0.9 # 90% на тренування, 10% на тест
split_index = int(len(X) * split_ratio)

X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

# Зміна форми X для LSTM
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

print(f"\nФорма X_train: {X_train.shape}")
print(f"Форма y_train: {y_train.shape}")
print(f"Форма X_test: {X_test.shape}")
print(f"Форма y_test: {y_test.shape}")

# --- 3. Побудова LSTM Моделі (можна залишити ту ж архітектуру для початку) ---

model = Sequential(name="NBU_Rate_LSTM_Forecast")
model.add(LSTM(units=64, return_sequences=True, input_shape=(n_steps, 1))) # Збільшимо трохи units
model.add(Dropout(0.2))
model.add(LSTM(units=64, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=32, activation='relu')) # Додамо ще один Dense шар
model.add(Dense(units=1))

# --- 4. Компіляція та Навчання Моделі ---

print("\nКомпіляція моделі...")
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
model.summary()

early_stopping = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True) # Збільшимо patience

print("\nПочаток навчання моделі...")
history = model.fit(X_train, y_train,
                    epochs=150, # Може знадобитись більше епох
                    batch_size=32,
                    validation_data=(X_test, y_test),
                    callbacks=[early_stopping],
                    verbose=1)

# --- 5. Прогнозування на Тестових Даних ---

print("\nСтворення прогнозів на тестових даних...")
predicted_scaled = model.predict(X_test)

# --- 6. Оцінка Моделі ---

# Повернення до оригінального масштабу
predicted_original = scaler.inverse_transform(predicted_scaled)
y_test_original = scaler.inverse_transform(y_test.reshape(-1, 1))

# Розрахунок метрик
rmse = np.sqrt(mean_squared_error(y_test_original, predicted_original))
mae = mean_absolute_error(y_test_original, predicted_original)

print("\nОцінка моделі на тестових даних (оригінальний масштаб):")
print(f"  Root Mean Squared Error (RMSE): {rmse:.4f} грн")
print(f"  Mean Absolute Error (MAE):    {mae:.4f} грн")

# Оцінка MAE у відсотках від середнього
mean_value_test = np.mean(y_test_original)
mape_like = (mae / mean_value_test) * 100 if mean_value_test != 0 else float('inf')
print(f"  Середнє значення на тесті: {mean_value_test:.4f} грн")
print(f"  Відносна середня абсолютна помилка (MAE / Mean): {mape_like:.2f}%")

# --- 7. Візуалізація Результатів ---

print("\nВізуалізація прогнозів...")

# Отримуємо відповідні дати для тестового набору
test_dates = df.index[len(data) - len(y_test):] # Дати для y_test_original

plt.figure(figsize=(14, 6))
plt.plot(test_dates, y_test_original, color='blue', label='Справжній курс НБУ (Actual)')
plt.plot(test_dates, predicted_original, color='red', linestyle='--', label='Прогнозований курс (Predicted)')
plt.title(f'Прогноз офіційного курсу {valcode}/UAH за допомогою LSTM')
plt.xlabel('Дата (тестовий період)')
plt.ylabel('Курс UAH')
plt.legend()
plt.grid(True)
plt.show()

# Графік втрат під час навчання (як і раніше)
plt.figure(figsize=(10, 4))
# Перевірка наявності ключів перед побудовою графіка
if 'loss' in history.history and 'val_loss' in history.history:
    plt.plot(history.history['loss'], label='Втрати на тренуванні (Training Loss)')
    plt.plot(history.history['val_loss'], label='Втрати на валідації (Validation Loss)')
    plt.title('Динаміка втрат під час навчання')
    plt.xlabel('Епохи')
    plt.ylabel('MSE Loss')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("Не вдалося побудувати графік втрат: відсутні дані в history.")

print("\n--- Завершення роботи ---")
print("**Нагадування:** Ця модель має обмежену прогнозну силу для реальних курсів НБУ.")

print("EXECUTION COMPLETED.")
# --- Кінець коду ---