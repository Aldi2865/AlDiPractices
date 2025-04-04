import tensorflow as tf
from tensorflow.keras.layers import Dense  # Імпортуємо повнозв'язний шар
from tensorflow.keras.models import Sequential # Імпортуємо послідовну модель
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Створення нейромережі
model = Sequential([
    # Вхідний шар: 64 нейрони, функція активації ReLU.
    # input_shape=(10,) означає, що модель очікує на вхід вектори з 10 елементів.
    Dense(64, activation='relu', input_shape=(10,)),

    # Прихований шар: 32 нейрони, функція активації ReLU.
    Dense(32, activation='relu'),

    # Вихідний шар: 1 нейрон (для бінарної класифікації),
    # функція активації sigmoid (виводить значення між 0 та 1, що інтерпретується як ймовірність).
    Dense(1, activation='sigmoid')
])

# Компільовуємо модель
model.compile(
    optimizer='adam', # Оптимізатор Adam - популярний та ефективний алгоритм оптимізації.
    loss='binary_crossentropy', # Функція втрат для бінарної класифікації.
    metrics=['accuracy'] # Метрика для оцінки якості моделі під час навчання та тестування.
)

# Виведення структури моделі: кількість шарів, їх параметри, загальна кількість параметрів.
model.summary()


# Генерація синтетичних даних
X, y = make_classification(n_samples=10000, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Навчання моделі
model.fit(X_train, y_train, epochs=20, batch_size=10, validation_data=(X_test, y_test))

#оцінка моделі
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Точність моделі: {accuracy:.2f}")
print(f"Втрати: {loss:.2f}")

