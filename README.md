### Скрипт для парсинга имен и телефонных номеров  с сайта avito.ru.

#### Начало работы

**Склонируйте репозиторий:** 
https://github.com/raptor72/AvitoPhonesParser

Установите зависимости:

```bash
pip install -r requirements.txt 
```

Для корректной работы скрипта необходимо, чтобы были установлены пакеты: **tesseract-ocr**, **libtesseract-dev**.

В config.py опция:

    user_agent

указывает user agent, который скрипт будет подставлять в get запросы.


Путь до файла в который будут записываться данные указывается в опции:

    logfile

Категория, в которой будет производиться поиск указывается в настройке:

    category_url

Это ссылка определенной категории на avito.ru. В примере используется поиск квартир в Москве.

Указать страницу с которой будет производится поиск можно опцией:

    page


