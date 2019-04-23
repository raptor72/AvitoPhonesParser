import requests
from bs4 import BeautifulSoup
import re
import base64
from PIL import Image
from pytesseract import image_to_string
from io import BytesIO
import random
from time import sleep

from config import *

base = 'https://www.avito.ru'


def phoneDemixer(key, id):
    pre = (re.findall('[\da-f]*', key))
    mixed = ''
    if int(id) % 2  == 0:
        for x in reversed(pre):
            mixed = mixed + x
    else:
        for x in pre:
            mixed = mixed + x
    s = len(mixed)
    r = ''
    for k in range(0, s):
        if k%3 == 0:
            r = r + mixed[k]
    return r


def get_html(url):
    useragent = {'User-Agent': user_agent}
    r = requests.get(url, headers=useragent)
    return r.text


def get_page_urls(html):
    res = []
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('div', class_='item_table-header')
    for i in links:
        j = i.find('a', class_='item-description-title-link').get('href')
        adv = base + j
        res.append(adv)
    return res


def get_adv_information(adv):
    html = get_html(adv)
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('div', class_='seller-info-name')
    addres = soup.find_all('div', class_='seller-info-prop')
    arr= []
    for i in reversed(addres):
        j = i.find('div', class_='seller-info-value')
        arr.append(j)
    adres = str(arr[0]).split('>')[1].split('<')[0].strip()
    name = str(name).split('>')[2].split('<')[0].strip()
    key = html.split("avito.item.phone")[1].split("'")[1]
    id = html.split("avito.item.id")[1].split("'")[1]
    hash = phoneDemixer(key, id)
    phone_url = 'https://www.avito.ru/items/phone/' + id + '?pkey=' + hash
    r = requests.get(phone_url, headers={'referer': adv, 'User-Agent': user_agent}, stream=True)
    img_data = bytes(str(r.content).split(";base64,")[1].split('"')[0].encode('utf-8'))
    image = Image.open(BytesIO(base64.b64decode(img_data)))
    phone = image_to_string(image).encode('utf-8')
#    print(adres)
    print(name)
    print(phone)
    log = open(logfile, 'a')
    log.write(adres + '; ')
    log.write(name + '; ')
    log.write(str(phone) + '; ')
    log.write(adv + '\n')
    log.close()


if __name__ == "__main__":
    for j in range(int(page), 100):
        url = category_url +  '?p=' + str(j) + '&user=1'
        print(url)
        for i in get_page_urls(get_html(url)):
            print(i)
            sleep(random.uniform(0.89, 3.92))
            get_adv_information(i)
