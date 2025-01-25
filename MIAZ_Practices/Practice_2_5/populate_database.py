import psycopg2
import pandas as pd
import os
from psycopg2 import sql
from pathlib import Path

def populate_database(excel_file, db_name, user, password, host, port):
  """Заповнює базу даних даними з файлу Excel."""
  conn = psycopg2.connect(database=db_name, user=user, password=password, host=host, port=port)
  cursor = conn.cursor()

  # Завантаження даних з Excel
  training_df = pd.read_excel(excel_file, sheet_name='Training_Personnel')
  programs_df = pd.read_excel(excel_file, sheet_name='Training_Programs')

  # Запис даних у таблицю Training_Programs
  for index, row in programs_df.iterrows():
      cursor.execute(
          sql.SQL("INSERT INTO Training_Programs (Training_Program_ID, Program_Name, Instructor, Start_Date, End_Date) VALUES (%s, %s, %s, %s, %s)"),
          (row['Training_Program_ID'], row['Program_Name'], row['Instructor'], row['Start_Date'], row['End_Date'])
      )

  # Запис даних у таблицю Training_Personnel
  for index, row in training_df.iterrows():
      cursor.execute(
          sql.SQL("INSERT INTO Training_Personnel (ID, Name, Rank, Training_Program_ID, Date_Enrolled) VALUES (%s, %s, %s, %s, %s)"),
          (row['ID'], row['Name'], row['Rank'], row['Training_Program_ID'], row['Date_Enrolled'])
      )


  conn.commit()
  cursor.close()
  conn.close()

if __name__ == "__main__":
  directory = os.path.dirname(os.path.abspath(__file__))
  excel_file = Path(directory) / 'training_data.xlsx'
  db_name = "MIAZ2025_Practice2_5"
  user = "postgres"  # Замініть на вашого користувача
  password = "admin"  # Замініть на ваш пароль
  host = "localhost"
  port = "5432"
  populate_database(excel_file, db_name, user, password, host, port)