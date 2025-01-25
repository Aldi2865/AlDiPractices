import subprocess
import os
import psycopg2
from pathlib import Path

def run_script(script_name):
  """Запускає python скрипт."""
  print(f"Running {script_name}...")
  try:
      subprocess.run(['python', script_name], check=True)
      print(f"Finished {script_name} successfully.\n")
  except subprocess.CalledProcessError as e:
      print(f"Error running {script_name}: {e}\n")

if __name__ == "__main__":
  directory = os.path.dirname(os.path.abspath(__file__))
  cr = Path(directory) / 'create_database.py'
  pd = Path(directory) / 'populate_database.py'
  qu = Path(directory) / 'sql_queries.py'
  run_script(cr)
  run_script(pd)
  run_script(qu)