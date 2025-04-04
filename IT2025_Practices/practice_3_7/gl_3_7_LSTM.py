import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense # type: ignore
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt # <-- Імпортуємо Matplotlib

# Встановлення random seed для відтворюваності (необов'язково, але корисно)
np.random.seed(42)
tf.random.set_seed(42)

# Побудова моделі LSTM для КЛАСИФІКАЦІЇ
model = Sequential([
    # Вхідна форма (timesteps, features_per_step)
    LSTM(50, activation='tanh', return_sequences=True, input_shape=(10, 1)),
    LSTM(50, activation='tanh'),
    Dense(1, activation='sigmoid')
])

# Компільовуємо модель для БІНАРНОЇ КЛАСИФІКАЦІЇ
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Генерація та підготовка даних
X, y = make_classification(n_samples=10000, n_features=10, n_informative=5, n_redundant=0, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Зміна форми даних для LSTM (кількість_зразків, кількість_кроків_часу, кількість_ознак_на_крок)
X_train_reshaped = X_train.reshape(-1, 10, 1)
X_test_reshaped = X_test.reshape(-1, 10, 1)

# Виведення інформації про модель (необов'язково)
model.summary()

# Навчання моделі
print("\nПочаток навчання моделі...")
epochs = 20 # Зберігаємо кількість епох у змінну
history = model.fit(X_train_reshaped, y_train,
                    epochs=epochs, # Використовуємо змінну epochs
                    batch_size=32, # Збільшено batch_size для більшої кількості даних
                    validation_data=(X_test_reshaped, y_test),
                    verbose=1)

# Оцінка моделі
print("\nОцінка моделі на тестових даних:")
loss, accuracy = model.evaluate(X_test_reshaped, y_test, verbose=0)

print(f"Втрати моделі (Loss): {loss:.4f}")
print(f"Точність моделі (Accuracy): {accuracy:.2f}")

# --- ПОБУДОВА ГРАФІКІВ ---

# Отримуємо дані з історії навчання
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

# Створюємо діапазон епох для осі X
epochs_range = range(epochs)

# Створюємо фігуру та осі для графіків
plt.figure(figsize=(14, 5)) # Задаємо розмір фігури для кращої візуалізації

# Графік точності
plt.subplot(1, 2, 1) # 1 рядок, 2 колонки, 1-й графік
plt.plot(epochs_range, acc, label='Точність на тренуванні (Training Accuracy)')
plt.plot(epochs_range, val_acc, label='Точність на валідації (Validation Accuracy)')
plt.legend(loc='lower right')
plt.title('Точність тренування та валідації')
plt.xlabel('Епохи')
plt.ylabel('Точність')
plt.grid(True) # Додаємо сітку

# Графік втрат
plt.subplot(1, 2, 2) # 1 рядок, 2 колонки, 2-й графік
plt.plot(epochs_range, loss, label='Втрати на тренуванні (Training Loss)')
plt.plot(epochs_range, val_loss, label='Втрати на валідації (Validation Loss)')
plt.legend(loc='upper right')
plt.title('Втрати тренування та валідації')
plt.xlabel('Епохи')
plt.ylabel('Втрати')
plt.grid(True) # Додаємо сітку

# Показуємо графіки
plt.tight_layout() # Автоматично налаштовує поля, щоб графіки не перекривалися
plt.show()
# --- КІНЕЦЬ БЛОКУ ГРАФІКІВ ---