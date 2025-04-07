import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import sqlalchemy # Для роботи з БД через pandas
import random # Для вибору підрозділів

print("\n--- Завдання 2 (PostgreSQL + Підрозділи): Етап 1 - Генерація та Запис, Етап 2 - Читання та Класифікація ---")

# --- Налаштування З'єднання з PostgreSQL ---
DB_NAME = "attack_classification_db"
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"

db_connection_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = None
try:
    engine = sqlalchemy.create_engine(db_connection_str)
    with engine.connect() as connection:
        print(f"Успішно підключено до PostgreSQL (База: {DB_NAME})")
except Exception as e:
    print(f"ПОМИЛКА підключення до PostgreSQL: {e}")
    exit()

# ==============================================================
# ЕТАП 1: Генерація Даних (з Підрозділами) та Запис у БД
# ==============================================================
print("\n--- ЕТАП 1: Генерація даних (з підрозділами) та Запис у БД ---")

# --- Генерація Даних ---
n_samples = 1000
n_features = 8
class_labels = {0: 'FPV', 1: 'Авіаційний удар'} # Типи ударів
possible_units = ['Яструби', 'Соколи', 'Тигри', 'Вовки', 'Леви'] # Список можливих підрозділів
n_classes = len(class_labels)

X, y = make_classification(
    n_samples=n_samples, n_features=n_features, n_informative=6,
    n_redundant=1, n_classes=n_classes, n_clusters_per_class=1,
    weights=[0.65, 0.35], flip_y=0.05, random_state=123
)
# Генеруємо випадковий підрозділ для кожного запису
units = np.random.choice(possible_units, size=n_samples)

print(f"Згенеровано {n_samples} записів з {n_features} ознаками та підрозділами.")

# --- Збереження Згенерованих Даних у БД (`attack_data_raw`) ---
raw_table_name = 'attack_data_raw'
print(f"Спроба збереження записів у таблицю '{raw_table_name}'...")
raw_feature_columns = [f'feature_{i+1}' for i in range(n_features)]
raw_data_df = pd.DataFrame(X, columns=raw_feature_columns)
raw_data_df['true_label_code'] = y
raw_data_df['unit_identifier'] = units # Додаємо колонку з підрозділами

try:
    raw_data_df.to_sql(raw_table_name, engine, if_exists='replace', index=False)
    print(f"Дані (з підрозділами) успішно збережено в таблицю '{raw_table_name}'.")
except Exception as e:
    print(f"ПОМИЛКА збереження даних у '{raw_table_name}': {e}")
    exit()

print("--- ЕТАП 1 Завершено ---")

# ==============================================================
# ЕТАП 2: Читання Даних з БД та Класифікація
# ==============================================================
print("\n--- ЕТАП 2: Читання даних з БД та Класифікація ---")

# --- Читання Даних з БД (`attack_data_raw`) ---
print(f"\nЧитання даних з таблиці '{raw_table_name}'...")
try:
    query = f"SELECT * FROM {raw_table_name}"
    data_from_db_df = pd.read_sql(query, engine)
    print(f"Успішно прочитано {len(data_from_db_df)} записів з '{raw_table_name}'.")

    # Розділяємо ознаки (X), мітки (y) та підрозділи (units)
    y_from_db = data_from_db_df['true_label_code'].values
    # НЕ включаємо 'unit_identifier' в ознаки X для моделі!
    X_from_db = data_from_db_df.drop(['true_label_code', 'unit_identifier'], axis=1).values
    units_from_db = data_from_db_df['unit_identifier'].values # Зберігаємо підрозділи окремо
    n_features_from_db = X_from_db.shape[1]

except Exception as e:
    print(f"ПОМИЛКА читання даних з '{raw_table_name}': {e}")
    exit()

# --- Підготовка та Навчання Моделі ---
print("\nПідготовка даних та навчання моделі...")
# Розділяємо X, y ТА units, зберігаючи відповідність
X_train, X_test, y_train, y_test, units_train, units_test = train_test_split(
    X_from_db, y_from_db, units_from_db, # Додаємо units_from_db до розділення
    test_size=0.3, random_state=42, stratify=y_from_db
)

# Масштабування лише ознак X
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Побудова та компіляція моделі (на вхід подаються лише ознаки)
model = Sequential([
    Dense(64, activation='relu', input_shape=(n_features_from_db,)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Навчання моделі (використовуємо лише X_train_scaled та y_train)
print("Навчання моделі...")
history = model.fit( X_train_scaled, y_train, epochs=60, batch_size=32, validation_split=0.15, verbose=0)
print("Модель навчено.")

# Оцінка
loss, accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Точність моделі на тестових даних: {accuracy*100:.2f}%")

# --- Прогноз для Тестових Даних (використовуємо лише X_test_scaled) ---
y_pred_probabilities = model.predict(X_test_scaled)
y_pred_classes = (y_pred_probabilities > 0.5).astype(int).flatten()
print("Прогноз для тестових даних отримано.")

# --- Створення DataFrame з Результатами (з Підрозділом) ---
print("Формування DataFrame з результатами класифікації...")
results_feature_columns = [f'feature_{i+1}' for i in range(n_features_from_db)]
# Створюємо DataFrame з НЕмасштабованих тестових ознак X_test
results_df = pd.DataFrame(X_test, columns=results_feature_columns)
# Додаємо відповідні підрозділи з units_test
results_df['Підрозділ'] = units_test
# Додаємо коди та текстові мітки класів
results_df['Справжній_Код'] = y_test
results_df['Прогнозований_Код'] = y_pred_classes
results_df['Удар_Справжній'] = results_df['Справжній_Код'].map(class_labels)
results_df['Удар_Прогноз'] = results_df['Прогнозований_Код'].map(class_labels)

# Перевпорядковуємо колонки для зручності
results_df = results_df[ ['Підрозділ', 'Удар_Справжній', 'Удар_Прогноз', 'Справжній_Код', 'Прогнозований_Код'] + results_feature_columns ]

# --- Збереження Результатів Класифікації у БД (`attack_data_classified`) ---
classified_table_name = 'attack_data_classified'
print(f"Спроба збереження {len(results_df)} результатів у таблицю '{classified_table_name}'...")
try:
    # Переконуємося, що назви колонок DataFrame відповідають назвам у CREATE TABLE
    # (Важливо для колонок з кирилицею/великими літерами, якщо використовували лапки в SQL)
    results_df.columns = ['Підрозділ', 'Удар_Справжній', 'Удар_Прогноз', 'Справжній_Код', 'Прогнозований_Код'] + results_feature_columns
    results_df.to_sql(classified_table_name, engine, if_exists='replace', index=False)
    print(f"Результати класифікації (з підрозділами) успішно збережено в '{classified_table_name}'.")
except Exception as e:
    print(f"ПОМИЛКА збереження результатів у '{classified_table_name}': {e}")
    # Можлива помилка через невідповідність назв колонок DataFrame та таблиці в БД
    print("Перевірте відповідність назв колонок у DataFrame та SQL CREATE TABLE.")
    exit()

# --- Виведення Прикладу Даних з Фінальної Таблиці ---
print("\n" + "="*80)
print(f"      Приклад даних з фінальної таблиці '{classified_table_name}' у PostgreSQL")
print("="*80)
try:
    final_query = f'SELECT * FROM "{classified_table_name}" LIMIT 10' # Використовуємо лапки для імені таблиці
    final_data_from_db = pd.read_sql(final_query, engine)
    # Використовуємо to_string() для кращого форматування в консолі
    print(final_data_from_db.to_string())
except Exception as e:
    print(f"ПОМИЛКА читання фінальних результатів з '{classified_table_name}': {e}")

print("\n" + "="*80)
print("--- ЕТАП 2 Завершено ---")

# Закриваємо з'єднання з БД
if engine:
    engine.dispose()
    print("\nЗ'єднання з PostgreSQL закрито.")