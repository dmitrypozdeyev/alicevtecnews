from bs4 import BeautifulSoup
import requests
url = 'https://t130631.spo.obrazovanie33.ru'



def getNewsDict():
    response = requests.get(f'{url}/news/')
    soup = BeautifulSoup(response.text, 'lxml')
    newsDict = {}
    for news in soup.find_all('h3', class_='events-card__title'):
        newsDict[news.text.lower()] = f'{url}{news.a.get("href")}'
    return newsDict



def getNewsText(url):
    resource = requests.get(url)
    soup = BeautifulSoup(resource.text, 'lxml')
    text = soup.find('div', class_='newsdetail-descr').text
    return text
