import psycopg2
import os
from psycopg2 import sql
from pathlib import Path


def execute_query(query, query_num, db_name, user, password, host, port):
  """Виконує SQL запит та зберігає результат у файл."""
  conn = psycopg2.connect(database=db_name, user=user, password=password, host=host, port=port)
  cursor = conn.cursor()

  cursor.execute(query)
  results = cursor.fetchall()

  directory = os.path.dirname(os.path.abspath(__file__))
  res_dir = Path(directory) / 'results'

  qf = Path(res_dir) / f'query_{query_num}.txt'

  with open(qf, 'w') as f:
    for row in results:
      f.write(str(row) + '\n')

  cursor.close()
  conn.close()

if __name__ == "__main__":
  db_name = "MIAZ2025_Practice2_5"
  user = "postgres"
  password = "admin" 
  host = "localhost"
  port = "5432"

  queries = [
    # 1. Вибрати імена та звання всього персоналу.
    "SELECT Name, Rank FROM Training_Personnel;",
    # 2. Знайти всі програми навчання, що тривають від Start_Date до End_Date включно.
    "SELECT * FROM Training_Programs;",
    # 3. Вибрати персонал, який проходить навчання за програмою з ID = 101.
    "SELECT * FROM Training_Personnel WHERE Training_Program_ID = 101;",
    # 4. Знайти персонал, який записався на навчання після 2024-01-12.
    "SELECT * FROM Training_Personnel WHERE Date_Enrolled > '2024-01-12';",
    # 5. Поєднати таблиці та вивести ім'я, звання та назву програми навчання.
    "SELECT tp.Name, tp.Rank, tpg.Program_Name FROM Training_Personnel tp JOIN Training_Programs tpg ON tp.Training_Program_ID = tpg.Training_Program_ID;",
    # 6. Знайти середню тривалість програм навчання (враховуючи End_Date - Start_Date).
     "SELECT AVG(End_Date - Start_Date) FROM Training_Programs;",
    # 7. Вибрати персонал зі званням "Lieutenant".
    "SELECT * FROM Training_Personnel WHERE Rank = 'Lieutenant';",
    # 8. Знайти програми навчання, на які ніхто не записаний.
    "SELECT tp.Program_Name FROM Training_Programs tp LEFT JOIN Training_Personnel tpers ON tp.Training_Program_ID = tpers.Training_Program_ID WHERE tpers.ID IS NULL;",
    # 9. Порахувати кількість персоналу, який проходить кожну програму навчання.
    "SELECT tpg.Program_Name, COUNT(tp.ID) FROM Training_Personnel tp JOIN Training_Programs tpg ON tp.Training_Program_ID = tpg.Training_Program_ID GROUP BY tpg.Program_Name;",
    # 10. Вибрати імена персоналу та назви програм, які тривають менше 15 днів.
    "SELECT tp.Name, tpg.Program_Name FROM Training_Personnel tp JOIN Training_Programs tpg ON tp.Training_Program_ID = tpg.Training_Program_ID WHERE tpg.End_Date - tpg.Start_Date < 15;",
    # 11. Знайти програму навчання з максимальною тривалістю.
    "SELECT * FROM Training_Programs ORDER BY (End_Date - Start_Date) DESC LIMIT 1;",
    # 12. Вибрати персонал з ідентифікатором програми навчання 102.
    "SELECT * FROM Training_Personnel WHERE Training_Program_ID = 102;",
    # 13. Вибрати імена інструкторів всіх програм
    "SELECT DISTINCT Instructor FROM Training_Programs",
    # 14. Вибрати персонал, ім'я якого починається на 'J'.
    "SELECT * FROM Training_Personnel WHERE Name LIKE 'J%';",
    # 15. Порахувати кількість різних програм навчання.
    "SELECT COUNT(DISTINCT Program_Name) FROM Training_Programs;",
    # 16. Вивести імена та звання персоналу, впорядковані за алфавітом по іменам.
    "SELECT Name, Rank FROM Training_Personnel ORDER BY Name ASC;",
    # 17. Вивести назву програми навчання та кількість персоналу на цій програмі для програм, де навчається більше 1 особи.
    "SELECT tpg.Program_Name, COUNT(*) FROM Training_Personnel tp JOIN Training_Programs tpg ON tp.Training_Program_ID = tpg.Training_Program_ID GROUP BY tpg.Program_Name HAVING COUNT(*) > 1;",
    # 18. Вивести мінімальну дату запису на кожну з програм
    "SELECT tpg.Program_Name, MIN(Date_Enrolled) FROM Training_Personnel tp JOIN Training_Programs tpg ON tp.Training_Program_ID = tpg.Training_Program_ID GROUP BY tpg.Program_Name",
    # 19. Вивести дати початку програм, впорядковані за зростанням
    "SELECT Start_Date FROM Training_Programs ORDER BY Start_Date ASC",
    # 20. Вивести імена та звання персоналу, що проходить навчання за програмою 'Basic Combat'
    "SELECT tp.Name, tp.Rank FROM Training_Personnel tp JOIN Training_Programs tpg ON tp.Training_Program_ID = tpg.Training_Program_ID WHERE tpg.Program_Name = 'Basic Combat'"
  ]

  for i, query in enumerate(queries):
      # Використання sql.SQL для уникнення SQL-ін'єкцій
      safe_query = sql.SQL(query)
      execute_query(safe_query, i + 1, db_name, user, password, host, port)