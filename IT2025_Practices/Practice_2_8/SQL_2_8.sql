-- Створення бази даних IT_2025_practice_2_8
CREATE DATABASE IT_2025_practice_2_8;

-- Перемикання на створену базу даних (не обов'язково, залежить від вашого клієнта SQL)
#\c IT_2025_practice_2_8;

-- Створення таблиці Units
CREATE TABLE Units (
    unit_id SERIAL PRIMARY KEY,
    unit_name VARCHAR(255) NOT NULL,
    unit_location VARCHAR(255)
);

-- Створення таблиці Operations
CREATE TABLE Operations (
    operation_id SERIAL PRIMARY KEY,
    operation_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    operation_status VARCHAR(50)
);

-- Створення таблиці Reports
CREATE TABLE Reports (
    report_id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    description TEXT,
    operation_id INT REFERENCES Operations(operation_id)
);

-- Створення таблиці зв'язку Units_Operations (M:N)
CREATE TABLE Units_Operations (
    unit_id INT REFERENCES Units(unit_id),
    operation_id INT REFERENCES Operations(operation_id),
    PRIMARY KEY (unit_id, operation_id)
);

-- Cтворення 1000 тестових записів для кожної таблиці з українськими назвами та описом.
-- 1. Таблиця Units (Підрозділи):
INSERT INTO Units (unit_name, unit_location)
SELECT
    'Підрозділ ' || (ROW_NUMBER() OVER ()),
    CASE
        WHEN (ROW_NUMBER() OVER ()) % 5 = 0 THEN 'Локація А'
        WHEN (ROW_NUMBER() OVER ()) % 5 = 1 THEN 'Локація Б'
        WHEN (ROW_NUMBER() OVER ()) % 5 = 2 THEN 'Локація В'
        WHEN (ROW_NUMBER() OVER ()) % 5 = 3 THEN 'Локація Г'
        ELSE 'Локація Д'
    END
FROM generate_series(1, 1000);

--2. Таблиця Operations (Операції):
INSERT INTO Operations (operation_name, start_date, end_date, operation_status)
SELECT
    'Операція ' || (ROW_NUMBER() OVER ()),
    CURRENT_DATE - (RANDOM() * 365)::INTEGER,
    CURRENT_DATE + (RANDOM() * 365)::INTEGER,
    CASE
        WHEN (ROW_NUMBER() OVER ()) % 4 = 0 THEN 'Заплановано'
        WHEN (ROW_NUMBER() OVER ()) % 4 = 1 THEN 'Виконується'
        WHEN (ROW_NUMBER() OVER ()) % 4 = 2 THEN 'Завершено'
        ELSE 'Скасовано'
    END
FROM generate_series(1, 1000);

--3. Таблиця Reports (Звіти):
INSERT INTO Reports (report_date, description, operation_id)
SELECT
    CURRENT_DATE - (RANDOM() * 365)::INTEGER,
    'Опис звіту ' || (ROW_NUMBER() OVER ()),
    (ROW_NUMBER() OVER ())
FROM generate_series(1, 1000);

--4. Таблиця Units_Operations (Підрозділи_Операції):
-- Цей спосіб генерує більше 1000 потенційних записів, а потім вибирає з них 1000 унікальних для уникнення помилки "обмеження унікальності "units_operations_pkey""
INSERT INTO Units_Operations (unit_id, operation_id)
SELECT unit_id, operation_id
FROM (
    SELECT DISTINCT
        (RANDOM() * 999)::INTEGER + 1 AS unit_id,
        (RANDOM() * 999)::INTEGER + 1 AS operation_id
    FROM generate_series(1, 2000) -- Генеруємо 2000 потенційних записів
) AS unique_combinations
LIMIT 1000;