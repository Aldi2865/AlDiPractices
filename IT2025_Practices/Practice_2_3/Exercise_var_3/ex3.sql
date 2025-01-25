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