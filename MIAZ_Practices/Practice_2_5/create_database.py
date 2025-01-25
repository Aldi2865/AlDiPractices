import psycopg2
from psycopg2 import sql

def create_database_and_tables(db_name, user, password, host, port):
  """Створює базу даних PostgreSQL та таблиці."""

  # Спочатку підключаємось до дефолтної БД postgres, щоб мати змогу створити нову
  conn_postgres = psycopg2.connect(database="postgres", user=user, password=password, host=host, port=port)
  conn_postgres.autocommit = True
  cursor_postgres = conn_postgres.cursor()

  # Перевіряємо, чи БД з вказаним іменем вже існує
  cursor_postgres.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), (db_name,))
  exists = cursor_postgres.fetchone()
  if not exists:
    # Створюємо базу даних
    cursor_postgres.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

  cursor_postgres.close()
  conn_postgres.close()

  # Підключаємось до новоствореної (або існуючої) бази даних
  conn = psycopg2.connect(database=db_name, user=user, password=password, host=host, port=port)
  cursor = conn.cursor()

  # Створення таблиці Training_Programs
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS Training_Programs (
      Training_Program_ID INTEGER PRIMARY KEY,
      Program_Name TEXT,
      Instructor TEXT,
      Start_Date DATE,
      End_Date DATE
    )
  ''')

  # Створення таблиці Training_Personnel
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS Training_Personnel (
      ID INTEGER PRIMARY KEY,
      Name TEXT,
      Rank TEXT,
      Training_Program_ID INTEGER,
      Date_Enrolled DATE,
      FOREIGN KEY (Training_Program_ID) REFERENCES Training_Programs(Training_Program_ID)
    )
  ''')



  conn.commit()
  cursor.close()
  conn.close()

if __name__ == "__main__":
  db_name = "MIAZ2025_Practice2_5"
  user = "postgres"  # Замініть на вашого користувача
  password = "admin"  # Замініть на ваш пароль
  host = "localhost"
  port = "5432"
  create_database_and_tables(db_name, user, password, host, port)