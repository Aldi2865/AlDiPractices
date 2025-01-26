-- Перевірка та створення бази даних
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'MIAZ2025_Practice2_5') THEN
    CREATE DATABASE "MIAZ2025_Practice2_5";
  END IF;
END $$;

-- Підключення до бази даних (не працює безпосередньо в .sql файлі, потрібно виконувати окремо)
-- \c "MIAZ2025_Practice2_5";

-- Створення таблиці Operations
CREATE TABLE IF NOT EXISTS Operations (
    Operation_ID INTEGER PRIMARY KEY,
    Operation_Name TEXT,
    Commander TEXT,
    Operation_Start_Date DATE,
    Operation_End_Date DATE
);

-- Створення таблиці Operations_Staff
CREATE TABLE IF NOT EXISTS Operations_Staff (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Role TEXT,
    Operation_ID INTEGER,
    Date_Assigned DATE,
    FOREIGN KEY (Operation_ID) REFERENCES Operations(Operation_ID)
);