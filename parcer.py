import requests
from bs4 import BeautifulSoup as bs

URL_TEMPLATE_START = "https://www.anekdot.ru/search/?query="
URL_TEMPLATE_END = "&ch%5Bj%5D=on&mode=any&xcnt=100&maxlen=&order=0"


def process_text(text):
    match = {
        '<div class="text">': '',
        '</div>': '',
        '.<br/>': ".\n",
        '!<br/>': "!\n",
        '?<br/>': "?\n",
        '\n<br/>': "\n\n",
        '<br/>': "",
        '<span style="background-color:#ffff80">': '',
        '</span>': '',
    }
    t = text
    for k in match:
        t = t.replace(k, match[k])
    return t


def parce(key_words):
    key_words = '+'.join(key_words.split())
    r = requests.get(URL_TEMPLATE_START + key_words + URL_TEMPLATE_END)
    soup = bs(r.text, "html.parser")
    anek_list = soup.find_all('div', class_='text')
    anek_list_text = []
    for anek in anek_list:
        text = process_text(str(anek))
        if len(text) >= 4095:
            continue
        else:
            anek_list_text.append(text)
    if not anek_list_text:
        return None
    return anek_list_text

list1 = parce('привет')
for i in list1:
    print(i)
    print('-------------------------------------------------------------')
