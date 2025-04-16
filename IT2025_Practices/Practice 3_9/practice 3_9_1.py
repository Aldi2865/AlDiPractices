import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, datasets, utils
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Завантаження та підготовка даних ---

# Завантажуємо набір даних CIFAR-10
(x_train, y_train), (x_test, y_test) = datasets.cifar10.load_data()

# Нормалізуємо значення пікселів до діапазону [0, 1]
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Перетворюємо мітки класів у формат one-hot encoding
num_classes = 10
y_train = utils.to_categorical(y_train, num_classes)
y_test = utils.to_categorical(y_test, num_classes)

# Визначаємо розмір вхідних даних (висота, ширина, канали)
input_shape = x_train.shape[1:] # (32, 32, 3)

# Назви класів (для наочності)
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

print(f"Розмір тренувальних даних: {x_train.shape}")
print(f"Розмір тестових даних: {x_test.shape}")
print(f"Кількість класів: {num_classes}")
print(f"Розмір вхідного зображення: {input_shape}")

# --- 2. Створення моделі CNN ---

model = keras.Sequential(
    [
        keras.Input(shape=input_shape), # Вхідний шар з визначеним розміром

        # Перший згортковий блок
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"), # Згортковий шар з 32 фільтрами
        layers.MaxPooling2D(pool_size=(2, 2)), # Шар підвибірки (пулінгу)

        # Другий згортковий блок
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"), # Згортковий шар з 64 фільтрами
        layers.MaxPooling2D(pool_size=(2, 2)), # Шар підвибірки

        # Вирівнювання даних перед повнозв'язними шарами
        layers.Flatten(),

        # Шар Dropout для регуляризації (зменшення перенавчання)
        layers.Dropout(0.5),

        # Повнозв'язний (Dense) шар
        layers.Dense(128, activation="relu"),

        # Вихідний шар з кількістю нейронів, що дорівнює кількості класів
        # Функція активації softmax для багатокласової класифікації
        layers.Dense(num_classes, activation="softmax"),
    ]
)

# Виводимо структуру моделі
model.summary()

# --- 3. Компіляція моделі ---

# Визначаємо функцію втрат, оптимізатор та метрики для оцінки
# 'categorical_crossentropy' - стандартна функція втрат для one-hot міток
# 'adam' - популярний оптимізатор
# 'accuracy' - метрика точності
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# --- 4. Тренування моделі ---

batch_size = 128  # Кількість зразків на одну ітерацію оновлення ваг
epochs = 15       # Кількість повних проходів по тренувальному набору даних

print("\nПочаток тренування моделі...")
# Запускаємо процес тренування
# validation_split=0.1 означає, що 10% тренувальних даних буде використано для валідації
history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    validation_split=0.1) # Використовуємо частину тренувальних даних для валідації

print("Тренування завершено.")

# --- 5. Оцінка моделі ---

# Оцінюємо продуктивність моделі на тестовому наборі даних
score = model.evaluate(x_test, y_test, verbose=0)
print(f"\nВтрати на тестових даних: {score[0]:.4f}")
print(f"Точність на тестових даних: {score[1]:.4f}")

# --- 6. (Опційно) Візуалізація історії тренування ---

plt.figure(figsize=(12, 4))

# Графік точності
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Точність на тренуванні')
plt.plot(history.history['val_accuracy'], label='Точність на валідації')
plt.title('Точність моделі')
plt.ylabel('Точність')
plt.xlabel('Епоха')
plt.legend(loc='lower right')

# Графік втрат
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Втрати на тренуванні')
plt.plot(history.history['val_loss'], label='Втрати на валідації')
plt.title('Втрати моделі')
plt.ylabel('Втрати')
plt.xlabel('Епоха')
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()