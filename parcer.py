import requests
from bs4 import BeautifulSoup as bs

URL_TEMPLATE = "https://www.anekdot.ru/search/?rubrika=j&query="


def parce(key_words):
    key_words = '+'.join(key_words.split())
    r = requests.get(URL_TEMPLATE + key_words)
    soup = bs(r.text, "html.parser")
    anek_list = soup.find_all('div', class_='text')
    anek_list_text = []
    for anek in anek_list:
        anek_list_text.append(anek.text)
    return anek_list_text
