# Завдання 2 (версія для 2 класів): Класифікація типу атаки (FPV vs Авіаудар)

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
# НЕ потрібен to_categorical для бінарної класифікації з одним вихідним нейроном
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("\n--- Завдання 2 (2 Класи): Бінарна класифікація (FPV vs Авіаційний удар) ---")

# 1. Генеруємо штучний набір даних для БІНАРНОЇ класифікації
# Припустимо, маємо 10 ознак для розрізнення між FPV атакою та авіаційним ударом
n_samples = 1200
n_features = 10
# Класи: 0 = FPV, 1 = Авіаційний удар
n_classes = 2

X, y = make_classification(
    n_samples=n_samples,
    n_features=n_features,
    n_informative=7, # Кількість інформативних ознак (напр., швидкість, висота, розмір об'єкту, РЕБ сигнал)
    n_redundant=1,   # Кількість надлишкових ознак
    n_repeated=0,    # Кількість повторюваних ознак
    n_classes=n_classes,
    n_clusters_per_class=1, # Припускаємо відносно чітке розділення
    weights=[0.6, 0.4], # Можна додати незбалансованість класів (напр., 60% FPV, 40% Авіаудари)
    random_state=42
)
print(f"Згенеровано {n_samples} прикладів з {n_features} ознаками для {n_classes} класів.")
print(f"Розподіл класів (0=FPV, 1=Авіаудар): {np.bincount(y)}")

# 2. Розділення вибірки
# Використовуємо оригінальний y (0/1)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y # stratify важливий при незбалансованих класах
)
print(f"Розмір тренувальної вибірки: {X_train.shape}, міток: {y_train.shape}")
print(f"Розмір тестової вибірки: {X_test.shape}, міток: {y_test.shape}")
print(f"Розподіл класів у тренувальній вибірці: {np.bincount(y_train)}")
print(f"Розподіл класів у тестовій вибірці: {np.bincount(y_test)}")


# 3. Масштабування даних
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Дані масштабовано за допомогою StandardScaler.")

# 4. Побудова моделі нейронної мережі для БІНАРНОЇ класифікації
model_attack_binary = Sequential([
    Dense(64, activation='relu', input_shape=(n_features,)), # Вхідний шар
    Dense(32, activation='relu'),                         # Прихований шар
    Dense(1, activation='sigmoid')                        # Вихідний шар (1 нейрон, sigmoid)
])

model_attack_binary.summary()

# 5. Компіляція моделі
model_attack_binary.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print("Модель скомпільовано (optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']).")

# 6. Навчання моделі
print("Починаємо навчання моделі...")
history_attack_binary = model_attack_binary.fit(
    X_train_scaled, y_train, # Передаємо y_train (0/1)
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=0 # Не виводити прогрес кожної епохи
)
print("Навчання завершено.")

# 7. Оцінка моделі на тестових даних
loss, accuracy = model_attack_binary.evaluate(X_test_scaled, y_test, verbose=0) # Передаємо y_test (0/1)
print(f"\nОцінка моделі на тестових даних:")
print(f"Loss: {loss:.4f}")
print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

# 8. Детальний звіт по класифікації та матриця плутанини
y_pred_probabilities = model_attack_binary.predict(X_test_scaled)
y_pred_classes = (y_pred_probabilities > 0.5).astype(int).flatten()

print("\nМатриця плутанини (Confusion Matrix):")
#      Predicted FPV | Predicted Авіаудар
#------------------------------------------
# True FPV      | TN          | FP
# True Авіаудар | FN          | TP
cm = confusion_matrix(y_test, y_pred_classes)
print(cm)
print(f"TN (Істинно FPV, спрогнозовано FPV):      {cm[0, 0]}")
print(f"FP (Істинно FPV, спрогнозовано Авіаудар): {cm[0, 1]}")
print(f"FN (Істинно Авіаудар, спрогнозовано FPV):  {cm[1, 0]}")
print(f"TP (Істинно Авіаудар, спрогнозовано Авіаудар): {cm[1, 1]}")


print("\nClassification Report:")
# Використовуємо оригінальні тестові мітки y_test
# Важливо: порядок імен має відповідати міткам 0 та 1
target_names = ['FPV', 'Авіаційний удар'] # 0 = FPV, 1 = Авіаційний удар
print(classification_report(y_test, y_pred_classes, target_names=target_names))

print("-" * 60)