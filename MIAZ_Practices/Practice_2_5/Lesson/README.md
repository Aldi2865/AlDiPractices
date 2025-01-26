Цей репозиторій містить код для практики з базами даних PostgreSQL, використовуючи дані про навчання військового персоналу. Код виконує наступні завдання:

1. **Створення бази даних PostgreSQL:** Скрипт створює базу даних `MIAZ2025_Practice2_5` (якщо вона ще не існує) та дві таблиці: `Training_Personnel` та `Training_Programs`.
2. **Заповнення бази даних з файлу Excel:** Дані з файлу `training_data.xlsx` завантажуються в таблиці `Training_Personnel` та `Training_Programs`.
3. **Виконання SQL запитів:** Скрипт виконує 20 різних SQL запитів для вибірки, фільтрації, групування та агрегації даних з бази. Результати кожного запиту зберігаються в окремому файлі в папці `results`.

**Структура репозиторію:**

```
personnel_training_postgres/
├── create_database.py        # Створення БД та таблиць у PostgreSQL
├── populate_database.py       # Заповнення БД з файлу Excel
├── sql_queries.py           # SQL запити
├── results/                  # Папка для збереження результатів запитів
│   ├── query_1.txt
│   ├── query_2.txt
│   ├── ...
│   └── query_20.txt
├── training_data.xlsx         # Файл Excel з даними
├── run_all.py                # Запуск всіх скриптів
└── README.md                 # Цей файл
```

**Вимоги:**

* Python 3.x
* PostgreSQL (з користувачем, який має права на створення БД)
* Бібліотеки Python:
  * `psycopg2-binary`
  * `pandas`

**Встановлення бібліотек:**

**Bash**

```
pip install psycopg2-binary pandas
```

**Підготовка даних:**

1. Створіть файл `training_data.xlsx` з двома листами: `Training_Personnel` та `Training_Programs`.
2. Заповніть листи даними згідно з наступною структурою:
   **Лист `Training_Personnel`:**| ID                                        | Name                | Rank            | Training_Program_ID | Date_Enrolled |
   | ----------------------------------------- | ------------------- | --------------- | ------------------- | ------------- |
   | 1                                         | John Doe            | Captain         | 101                 | 2024-01-10    |
   | 2                                         | Jane Smith          | Lieutenant      | 102                 | 2024-01-12    |
   | 3                                         | Mike Johnson        | Sergeant        | 101                 | 2024-01-15    |
   | 4                                         | Anna Brown          | Lieutenant      | 103                 | 2024-02-01    |
   | 5                                         | Chris Green         | Sergeant        | 102                 | 2024-02-05    |
   | **Лист `Training_Programs`:** |                     |                 |                     |               || Training_Program_ID | Program_Name     | Instructor    | Start_Date | End_Date   |
   | ------------------- | ---------------- | ------------- | ---------- | ---------- |
   | 101                 | Basic Combat     | Maj. Winters  | 2024-01-05 | 2024-01-20 |
   | 102                 | Advanced Tactics | Capt. Winters | 2024-01-10 | 2024-01-25 |
   | 103                 | Medical Aid      | Sgt. Hartman  | 2024-02-01 | 2024-02-15 |

**Налаштування:**

1. Відкрийте файли `create_database.py`, `populate_database.py` та `sql_queries.py`.
2. Замініть значення змінних `user`, `password`, `host` та `port` на ваші облікові дані для підключення до PostgreSQL.

**Використання:**

1. **Запустіть файл `run_all.py`** . Цей скрипт послідовно виконає:

* `create_database.py`
* `populate_database.py`
* `sql_queries.py`

1. Результати SQL запитів будуть збережені в папці `results`.

**Додатково:**

* Ви можете запускати кожен файл окремо, якщо вам потрібно виконати тільки певну частину роботи.

---
