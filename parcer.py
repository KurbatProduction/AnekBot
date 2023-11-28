import requests
from bs4 import BeautifulSoup as bs

URL_TEMPLATE_START = "https://www.anekdot.ru/search/?query="
URL_TEMPLATE_END = "&ch%5Bj%5D=on&mode=any&xcnt=100&maxlen=&order=0"


def parce(key_words):
    key_words = '+'.join(key_words.split())
    r = requests.get(URL_TEMPLATE_START + key_words + URL_TEMPLATE_END)
    soup = bs(r.text, "html.parser")
    anek_list = soup.find_all('div', class_='text')
    anek_list_text = []
    for anek in anek_list:
        if len(anek.text) >= 4095:
            continue
        else:
            anek_list_text.append(anek.text)
    if not anek_list_text:
        return None
    return anek_list_text
