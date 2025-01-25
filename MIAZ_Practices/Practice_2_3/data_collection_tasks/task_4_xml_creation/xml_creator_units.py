# xml_creator.py
import xml.etree.ElementTree as ET
import random
import os

def generate_unit_name():
  """Генерує випадкову назву підрозділу."""
  prefixes = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet",
              "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango",
              "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"]
  suffixes = ["Squad", "Team", "Group", "Platoon", "Company", "Battalion", "Regiment", "Division", "Corps", "Army"]
  return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def create_unit_xml(units):
  """
  Створює XML-файл з даними про підрозділи.

  Args:
    units: Список словників, де кожен словник містить дані про один підрозділ.
           Кожен словник повинен мати ключі "quantity", "status".
           (Ключ "name" буде згенеровано автоматично)
  """

  root = ET.Element("units")

  existing_names = set() # Створюємо множину для відстеження унікальності імен

  for unit_data in units:
    unit_element = ET.SubElement(root, "unit")

    # Генеруємо унікальну назву для кожного підрозділу
    name = generate_unit_name()
    while name in existing_names:
      name = generate_unit_name()
    existing_names.add(name)
    
    name_element = ET.SubElement(unit_element, "name")
    name_element.text = name

    quantity_element = ET.SubElement(unit_element, "quantity")
    quantity_element.text = str(unit_data["quantity"])

    status_element = ET.SubElement(unit_element, "status")
    status_element.text = unit_data["status"]

    tree = ET.ElementTree(root)
    fileName = 'unit_data.xml'
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, fileName)
  tree.write(file, encoding="utf-8", xml_declaration=True)

# Тестові дані (без ключа "name")
units_data = [
    {"quantity": 150, "status": "Active"},
    {"quantity": 120, "status": "Standby"},
    {"quantity": 80, "status": "Active"},
    {"quantity": 95, "status": "Training"},
    {"quantity": 110, "status": "Active"},
    {"quantity": 60, "status": "Maintenance"},
    {"quantity": 75, "status": "Active"},
    {"quantity": 130, "status": "Standby"},
    {"quantity": 90, "status": "Active"},
    {"quantity": 100, "status": "Training"},
]

# Створення XML-файлу
create_unit_xml(units_data)