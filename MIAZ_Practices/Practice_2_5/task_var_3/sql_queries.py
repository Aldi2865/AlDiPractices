import psycopg2
from psycopg2 import sql
import os
from config import Config  # Імпортуємо клас Config

def execute_query(query, query_num, config):
    """Виконує SQL запит та зберігає результат у файл."""
    conn = None  # Ініціалізуємо conn
    try:
        conn = psycopg2.connect(database=config.db_name, user=config.user, password=config.password, host=config.host, port=config.port)
        cursor = conn.cursor()

        cursor.execute(query)
        results = cursor.fetchall()

        # Створення папки results у поточній директорії, якщо її немає
        results_dir = os.path.join(config.current_dir, 'results') # Змінений шлях
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        with open(os.path.join(results_dir, f'query_{query_num}.txt'), 'w') as f:
            # Записуємо текст запиту у файл
            f.write(f"-- Query {query_num}:\n")
            f.write(f"{query.as_string(conn)}\n\n")  # Використовуємо .as_string(conn) для коректного форматування

            # Записуємо результати запиту
            for row in results:
                f.write(str(row) + '\n')

        cursor.close()

    except psycopg2.Error as e:
        print(f"Помилка при роботі з PostgreSQL: {e}")
    except OSError as e:
        print(f"Помилка при роботі з файловою системою: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Створення об'єкту Config
    config = Config()

    print(f"Використовується інтерпретатор: {config.python_exe}")

    queries = [
        # 1. Вибрати імена та ролі всього персоналу.
        "SELECT Name, Role FROM Operations_Staff;",
        # 2. Знайти всі операції, які починаються у квітні 2024 року.
        "SELECT * FROM Operations WHERE Operation_Start_Date BETWEEN '2024-04-01' AND '2024-04-30';",
        # 3. Вибрати персонал, призначений на операцію з ID = 1.
        "SELECT * FROM Operations_Staff WHERE Operation_ID = 1;",
        # 4. Знайти операції, якими керує Maj. Winters.
        "SELECT * FROM Operations WHERE Commander = 'Maj. Winters';",
        # 5. Поєднати таблиці та вивести ім'я, роль та назву операції.
        "SELECT os.Name, os.Role, o.Operation_Name FROM Operations_Staff os JOIN Operations o ON os.Operation_ID = o.Operation_ID;",
        # 6. Знайти середню тривалість операцій.
        "SELECT AVG(Operation_End_Date - Operation_Start_Date) FROM Operations;",
        # 7. Вибрати персонал з роллю 'Coordinator'.
        "SELECT * FROM Operations_Staff WHERE Role = 'Coordinator';",
        # 8. Знайти операції, які закінчуються після 2024-04-25.
        "SELECT * FROM Operations WHERE Operation_End_Date > '2024-04-25';",
        # 9. Порахувати кількість персоналу, задіяного в кожній операції.
        "SELECT o.Operation_Name, COUNT(os.ID) FROM Operations_Staff os JOIN Operations o ON os.Operation_ID = o.Operation_ID GROUP BY o.Operation_Name;",
        # 10. Вибрати імена персоналу та дати призначення для операцій, що тривають менше 15 днів.
        "SELECT os.Name, os.Date_Assigned FROM Operations_Staff os JOIN Operations o ON os.Operation_ID = o.Operation_ID WHERE o.Operation_End_Date - o.Operation_Start_Date < 15;",
        # 11. Знайти операцію з максимальною тривалістю.
        "SELECT * FROM Operations ORDER BY (Operation_End_Date - Operation_Start_Date) DESC LIMIT 1;",
        # 12. Вибрати персонал з ідентифікатором операції 2.
        "SELECT * FROM Operations_Staff WHERE Operation_ID = 2;",
        # 13. Вивести список всіх унікальних імен командирів
        "SELECT DISTINCT Commander FROM Operations",
        # 14. Вибрати персонал, ім'я якого починається на 'A'.
        "SELECT * FROM Operations_Staff WHERE Name LIKE 'A%';",
        # 15. Порахувати кількість різних ролей персоналу.
        "SELECT COUNT(DISTINCT Role) FROM Operations_Staff;",
        # 16. Вивести імена та ролі персоналу, впорядковані за алфавітом по іменам.
        "SELECT Name, Role FROM Operations_Staff ORDER BY Name ASC;",
        # 17. Вивести назву операції та кількість персоналу, задіяного в ній, для операцій з кількістю персоналу більше 1.
        "SELECT o.Operation_Name, COUNT(os.ID) FROM Operations_Staff os JOIN Operations o ON os.Operation_ID = o.Operation_ID GROUP BY o.Operation_Name HAVING COUNT(os.ID) > 1;",
        # 18. Вивести мінімальну дату початку операції
        "SELECT MIN(Operation_Start_Date) FROM Operations",
        # 19. Вивести дати завершення операцій, впорядковані за зростанням
        "SELECT Operation_End_Date FROM Operations ORDER BY Operation_End_Date ASC",
        # 20. Вивести імена та ролі персоналу, що задіяний в операції 'Alpha'
         "SELECT os.Name, os.Role FROM Operations_Staff os JOIN Operations o ON os.Operation_ID = o.Operation_ID WHERE o.Operation_Name = 'Alpha'"
    ]

    for i, query in enumerate(queries):
        # Використання sql.SQL для уникнення SQL-ін'єкцій
        safe_query = sql.SQL(query)
        execute_query(safe_query, i + 1, config)