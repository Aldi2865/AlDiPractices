import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL сторінки новин КНУ
url = "https://knu.ua/ua/"

# Виконання запиту на сайт
response = requests.get(url)
response.encoding = 'utf-8'  # Встановлення кодування для коректного відображення українських символів

# Перевірка статусу відповіді
if response.status_code == 200:
    # Створення об'єкта BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Пошук всіх елементів, що містять заголовки новин
    headlines = []
    for item in soup.find_all('p', class_='b-news__content'):
        title = item.get_text(strip=True)
        headlines.append({'Заголовок': title})
    
    # Створення DataFrame для збереження заголовків
    df = pd.DataFrame(headlines)
    
    # Збереження у CSV-файл
    fileName = 'news_titles.csv'
    directory = os.path.dirname(__file__)
    file = os.path.join(directory, fileName)
    print(file)
    df.to_csv(file, index=False, encoding='utf-8')
    msg = f"Заголовки збережено у файл {fileName}"

    print(msg)
else:
    print(f"Не вдалося отримати доступ до сайту. Статус код: {response.status_code}")