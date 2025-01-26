import psycopg2
from psycopg2 import sql
from config import Config  # Імпортуємо клас Config

def create_database_and_tables(config):
    """Створює базу даних PostgreSQL та таблиці."""
    conn_postgres = None  # Ініціалізуємо conn_postgres
    try:
        # Спочатку підключаємось до дефолтної БД postgres, щоб мати змогу створити нову
        conn_postgres = psycopg2.connect(database="postgres", user=config.user, password=config.password, host=config.host, port=config.port)
        conn_postgres.autocommit = True
        cursor_postgres = conn_postgres.cursor()

        # Перевіряємо, чи БД з вказаним іменем вже існує
        cursor_postgres.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), (config.db_name,))
        exists = cursor_postgres.fetchone()
        if not exists:
            # Створюємо базу даних
            cursor_postgres.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config.db_name)))

        # Підключаємось до новоствореної (або існуючої) бази даних
        conn = psycopg2.connect(database=config.db_name, user=config.user, password=config.password, host=config.host, port=config.port)
        cursor = conn.cursor()

        # Створення таблиці Operations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Operations (
                Operation_ID INTEGER PRIMARY KEY,
                Operation_Name TEXT,
                Commander TEXT,
                Operation_Start_Date DATE,
                Operation_End_Date DATE
            )
            ''')

        # Створення таблиці Operations_Staff
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Operations_Staff (
                ID INTEGER PRIMARY KEY,
                Name TEXT,
                Role TEXT,
                Operation_ID INTEGER,
                Date_Assigned DATE,
                FOREIGN KEY (Operation_ID) REFERENCES Operations(Operation_ID)
            )
            ''')

        conn.commit()
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Помилка при роботі з PostgreSQL: {e}")
    finally:
        if conn_postgres:
            cursor_postgres.close()
            conn_postgres.close()

if __name__ == "__main__":
    # Створення об'єкту Config
    config = Config()

    print(f"Використовується інтерпретатор: {config.python_exe}")
    create_database_and_tables(config)