import requests
from bs4 import BeautifulSoup
import json
import os

# URL сторінки новин КНУ
url = "https://knu.ua/ua/"

# Ключові слова для фільтрації
keywords = ["технології", "наука", "інновації", "дослідження", "університет", "студенти"]

# Виконання запиту на сайт
response = requests.get(url)
response.encoding = 'utf-8'

# Перевірка статусу відповіді
if response.status_code == 200:
    # Створення об'єкта BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Пошук всіх елементів, що містять заголовки новин
    headlines = []
    for item in soup.find_all('p', class_='b-news__content'):
        title = item.get_text(strip=True)
        # Перевірка наявності ключових слів у заголовку
        if any(keyword.lower() in title.lower() for keyword in keywords):
            headlines.append({'Заголовок': title})

    # Збереження у JSON-файл
    fileName = 'news_titles_filtered.json'
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, fileName)
    print(file)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(headlines, f, ensure_ascii=False, indent=4)

    msg = f"Заголовки, що містять ключові слова: {', '.join(keywords)}, збережено у файл {fileName}"

    print(msg)
else:
    print(f"Не вдалося отримати доступ до сайту. Статус код: {response.status_code}")