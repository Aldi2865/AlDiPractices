import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler # Додано для масштабування даних
from tensorflow.keras.layers import LeakyReLU # Додано для використання LeakyReLU
from tensorflow.keras.optimizers import Adam # Додано для використання Adam оптимізатора
from tensorflow.keras.callbacks import EarlyStopping # Додано для ранньої зупинки навчання
from tensorflow.keras.layers import BatchNormalization # Додано для нормалізації пакетів
from sklearn.metrics import classification_report, confusion_matrix # Додано для оцінки моделі

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
model.add(Dense(64,  input_shape=(n_features,), name="Hidden_Layer_1"))
model.add(BatchNormalization())
# model.add(Activation('relu')) # Використовувати ReLU
model.add(LeakyReLU(alpha=0.01)) # Використовувати LeakyReLU замість activation='relu'

# Другий прихований шар: 32 нейрони, функція активації ReLU
model.add(Dense(32, activation='relu', name="Hidden_Layer_2"))

model.add(LeakyReLU(alpha=0.01)) # Використовувати LeakyReLU замість activation='relu'

# Вихідний шар: кількість нейронів = кількість класів (n_classes)
# Функція активації 'softmax' для багатокласової класифікації (видає ймовірності для кожного класу)
model.add(Dense(n_classes, activation='softmax', name="Output_Layer"))

# --- 4. Компіляція моделі ---

# Оптимізатор: 'adam' - популярний та ефективний вибір
# Функція втрат: 'sparse_categorical_crossentropy' - підходить, коли мітки класів (y) є цілими числами (0, 1, 2...).
# Якщо б мітки були у форматі one-hot encoding (напр., [1,0,0], [0,1,0]), використовували б 'categorical_crossentropy'.
# Метрики: 'accuracy' - відсоток правильно класифікованих зразків
# optimizer = Adam(learning_rate=0.0005) # Спробуйте менше значення
optimizer = Adam(learning_rate=0.001) # Спробуйте менше значення
model.compile(optimizer=optimizer, # Використовуємо Adam для регуляризації
              # learning_rate=0.001, # Залишаємо за замовчуванням
              # optimizer='adam', # Залишаємо Adam для порівняння
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Виведення структури моделі
model.summary()

# --- 5. Навчання моделі ---

# epochs = 50 # Кількість епох навчання
epochs = 200 # Кількість епох навчання
batch_size = 32 # Розмір міні-пакета даних на кожній ітерації

print("\nПочаток навчання моделі...")
early_stopping = EarlyStopping(monitor='val_loss', # Стежити за втратами на валідації
                               patience=10,        # Кількість епох без покращення перед зупинкою
                               restore_best_weights=True) # Відновити найкращі ваги моделі
# validation_data дозволяє відстежувати продуктивність на тестовому наборі після кожної епохи
history = model.fit(X_train, y_train,
                    epochs=epochs,
                    batch_size=batch_size,
                    validation_data=(X_test, y_test),
                    callbacks=[early_stopping], # Додаємо ранню зупинку
                    verbose=1) # verbose=1 показує прогрес навчання

# --- 6. Оцінка моделі ---

print("\nОцінка моделі на тестових даних:")
loss, accuracy = model.evaluate(X_test, y_test, verbose=0) # verbose=0 приховує виведення під час оцінки

print(f"Втрати моделі на тесті (Test Loss): {loss:.4f}")
print(f"Точність моделі на тесті (Test Accuracy): {accuracy:.4f}")

# --- (Додатково) Прогнозування на нових даних ---

print("\n\n--- Прогнозування на прикладі декількох зразків з тестового набору ---")

# Кількість зразків для прикладу прогнозування
num_samples_to_predict = 10 # Можете змінити це число

if len(X_test) >= num_samples_to_predict:
    # Вибираємо перші 'num_samples_to_predict' зразків з тестового набору
    # Важливо: X_test має містити дані, вже масштабовані за допомогою scaler!
    sample_data_to_predict = X_test[:num_samples_to_predict]
    true_labels_for_samples = y_test[:num_samples_to_predict]

    # Отримуємо прогнози від моделі
    # model.predict() повертає масив ймовірностей для кожного класу
    predicted_probabilities = model.predict(sample_data_to_predict)

    # Щоб отримати остаточний прогнозований клас, знаходимо індекс (клас)
    # з найвищою ймовірністю для кожного зразка
    predicted_classes = np.argmax(predicted_probabilities, axis=1)

    # Виводимо результати для порівняння
    print(f"\nПрогнозування для перших {num_samples_to_predict} зразків:")
    print("-" * 30)
    for i in range(num_samples_to_predict):
        print(f"Зразок {i+1}:")
        print(f"  Справжній клас: {true_labels_for_samples[i]}")
        print(f"  Прогнозований клас: {predicted_classes[i]}")
        # Виводимо ймовірності, заокруглені для кращої читабельності
        print(f"  Прогнозовані ймовірності (класи 0, 1, 2): {np.round(predicted_probabilities[i], 3)}")
        print("-" * 10)

else:
    print(f"Недостатньо даних у тестовому наборі ({len(X_test)}) для вибору {num_samples_to_predict} зразків.")

# --- Кінець блоку прогнозування ---

# --- 7. Візуалізація процесу навчання ---

print("\nПобудова графіків процесу навчання...")

# Отримуємо дані з історії навчання
# Кількість епох, які реально були пройдені (може бути менше за epochs через EarlyStopping)
actual_epochs = len(history.history['loss'])
epochs_range = range(actual_epochs)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

# Створюємо фігуру та осі для графіків
plt.figure(figsize=(14, 5)) # Задаємо розмір фігури для кращої візуалізації

# Графік точності
plt.subplot(1, 2, 1) # 1 рядок, 2 колонки, 1-й графік
plt.plot(epochs_range, acc, label='Точність на тренуванні (Training Accuracy)')
plt.plot(epochs_range, val_acc, label='Точність на валідації (Validation Accuracy)')
plt.legend(loc='lower right')
plt.title('Точність тренування та валідації')
plt.xlabel(f'Епохи (зупинено на {actual_epochs})')
plt.ylabel('Точність')
plt.grid(True) # Додаємо сітку

# Графік втрат
plt.subplot(1, 2, 2) # 1 рядок, 2 колонки, 2-й графік
plt.plot(epochs_range, loss, label='Втрати на тренуванні (Training Loss)')
plt.plot(epochs_range, val_loss, label='Втрати на валідації (Validation Loss)')
plt.legend(loc='upper right')
plt.title('Втрати тренування та валідації')
plt.xlabel(f'Епохи (зупинено на {actual_epochs})')
plt.ylabel('Втрати')
plt.grid(True) # Додаємо сітку

# Показуємо графіки
plt.tight_layout() # Автоматично налаштовує поля, щоб графіки не перекривалися
plt.show()
# --- КІНЕЦЬ БЛОКУ ГРАФІКІВ ---

# --- (Додатково) Оцінка за допомогою Classification Report та Confusion Matrix ---

print("\nДетальна оцінка моделі:")
# Отримуємо прогнози для тестового набору
y_pred_probabilities = model.predict(X_test)
y_pred = np.argmax(y_pred_probabilities, axis=1) # Беремо клас з найвищою ймовірністю

# Classification Report (точність, повнота, F1-score для кожного класу)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix (матриця помилок)
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
# -------------------------------------------------------------------------------