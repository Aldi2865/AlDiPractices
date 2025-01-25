# xml_creator.py
import xml.etree.ElementTree as ET
import random
import os

def generate_resource_name():
    """Генерує випадкову назву ресурсу."""
    prefixes = ["Light", "Heavy", "Armored", "Combat", "Support", "Recon", "Medical", "Transport", "Engineering", "Communication"]
    suffixes = ["Vehicle", "Truck", "Tank", "APC", "Helicopter", "Drone", "Generator", "Radio", "Ambulance", "Bulldozer", "Excavator"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def create_resource_xml(resources):
    """
    Створює XML-файл з даними про ресурси.

    Args:
        resources: Список словників, де кожен словник містить дані про один ресурс.
                   Кожен словник повинен мати ключі "quantity", "availability".
                   (Ключ "name" буде згенеровано автоматично)
    """

    root = ET.Element("resources")

    existing_names = set()  # Створюємо множину для відстеження унікальності імен

    for resource_data in resources:
        resource_element = ET.SubElement(root, "resource")

        # Генеруємо унікальну назву для кожного ресурсу
        name = generate_resource_name()
        while name in existing_names:
            name = generate_resource_name()
        existing_names.add(name)

        name_element = ET.SubElement(resource_element, "name")
        name_element.text = name

        quantity_element = ET.SubElement(resource_element, "quantity")
        quantity_element.text = str(resource_data["quantity"])

        availability_element = ET.SubElement(resource_element, "availability")
        availability_element.text = resource_data["availability"]

    tree = ET.ElementTree(root)
    file_name = 'resource_data.xml'
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, file_name)
    tree.write(file, encoding="utf-8", xml_declaration=True)

# Тестові дані (без ключа "name", "availability" замість "status")
resources_data = [
    {"quantity": 10, "availability": "Available"},
    {"quantity": 5, "availability": "In Repair"},
    {"quantity": 2, "availability": "Available"},
    {"quantity": 8, "availability": "Available"},
    {"quantity": 3, "availability": "Maintenance"},
    {"quantity": 15, "availability": "Available"},
    {"quantity": 7, "availability": "Available"},
    {"quantity": 1, "availability": "In Repair"},
    {"quantity": 4, "availability": "Available"},
    {"quantity": 6, "availability": "Available"},
]

# Створення XML-файлу
create_resource_xml(resources_data)