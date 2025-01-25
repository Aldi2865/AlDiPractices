````markdown
# Генератор XML-файлів для даних про підрозділи та ресурси

Цей репозиторій містить дві версії скрипту Python, які генерують XML-файли з даними:

*   **Версія 1:** Дані про військові підрозділи.
*   **Версія 2:** Дані про ресурси (наприклад, транспортні засоби або обладнання).

## Версії скриптів

*   **`xml_creator_units.py` (Версія 1):** Цей скрипт генерує XML-файл з даними про військові підрозділи, включаючи їхні назви, кількість особового складу та статус.
*   **`xml_creator_resources.py` (Версія 2):** Цей скрипт генерує XML-файл з даними про ресурси, включаючи їхні назви, кількість та доступність.

## Використання

### Загальні кроки

1.  **Встановлення залежностей:**
    ```bash
    pip install xml
    ```
    (Зазвичай `xml` входить до стандартної бібліотеки Python)

2.  **Налаштування даних:**
    *   **Для `xml_creator_units.py`:** Відредагуйте список `units_data` у файлі. Кожен словник у списку представляє один підрозділ і має такі ключі:
        *   `"quantity"`: Ціле число, що вказує кількість особового складу.
        *   `"status"`: Рядок, що описує статус підрозділу (наприклад, "Active", "Standby", "Training").
    *   **Для `xml_creator_resources.py`:** Відредагуйте список `resources_data` у файлі. Кожен словник у списку представляє один ресурс і має такі ключі:
        *   `"quantity"`: Ціле число, що вказує кількість ресурсу.
        *   `"availability"`: Рядок, що описує доступність ресурсу (наприклад, "Available", "In Repair", "Maintenance").

3.  **Запуск скрипту:**
    ```bash
    python xml_creator.py
    ```

### Результат

*   **`xml_creator_units.py`:** Створить файл `unit_data.xml` у тому ж каталозі.
*   **`xml_creator_resources.py`:** Створить файл `resource_data.xml` у тому ж каталозі.

## Структура XML

### `unit_data.xml` (Версія 1)

```xml
<?xml version="1.0" encoding="utf-8"?>
<units>
  <unit>
    <name>Назва підрозділу 1</name>
    <quantity>Кількість</quantity>
    <status>Статус</status>
  </unit>
  <unit>
    <name>Назва підрозділу 2</name>
    <quantity>Кількість</quantity>
    <status>Статус</status>
  </unit>
  ...
</units>
````

* `<units>`: Кореневий елемент.
* `<unit>`: Кожен елемент `<unit>` представляє один підрозділ.
  * `<name>`: Назва підрозділу (генерується випадковим чином).
  * `<quantity>`: Кількість особового складу.
  * `<status>`: Статус підрозділу.

### `resource_data.xml` (Версія 2)

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
  <resource>
    <name>Назва ресурсу 1</name>
    <quantity>Кількість</quantity>
    <availability>Доступність</availability>
  </resource>
  <resource>
    <name>Назва ресурсу 2</name>
    <quantity>Кількість</quantity>
    <availability>Доступність</availability>
  </resource>
  ...
</resources>
```

* `<resources>`: Кореневий елемент.
* `<resource>`: Кожен елемент `<resource>` представляє один тип ресурсу.
  * `<name>`: Назва ресурсу (генерується випадковим чином).
  * `<quantity>`: Кількість ресурсу.
  * `<availability>`: Статус доступності ресурсу.

## Функції

### Версія 1 (`xml_creator_units.py`)

* `generate_unit_name()`: Генерує випадкову назву підрозділу, використовуючи комбінацію префіксів (Alpha, Bravo, etc.) та суфіксів (Squad, Platoon, etc.).
* `create_unit_xml(units)`: Приймає список словників `units` і створює XML-файл `unit_data.xml`.

### Версія 2 (`xml_creator_resources.py`)

* `generate_resource_name()`: Генерує випадкову назву ресурсу, використовуючи комбінацію префіксів та суфіксів, що описують типи техніки та обладнання.
* `create_resource_xml(resources)`: Приймає список словників `resources` і створює XML-файл `resource_data.xml`.

## Приклади згенерованих XML

### `unit_data.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<units>
  <unit>
    <name>Alpha Platoon</name>
    <quantity>150</quantity>
    <status>Active</status>
  </unit>
  <unit>
    <name>Bravo Company</name>
    <quantity>120</quantity>
    <status>Standby</status>
  </unit>
  ...
</units>
```

### `resource_data.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
  <resource>
    <name>Light Tank</name>
    <quantity>10</quantity>
    <availability>Available</availability>
  </resource>
  <resource>
    <name>Combat Ambulance</name>
    <quantity>5</quantity>
    <availability>In Repair</availability>
  </resource>
  ...
</resources>
```
