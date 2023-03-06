# Проект Shops
## Автор
Аберхаев Альберт
## Задание
### Цель:
Реализовать сервис, который принимает и отвечает на HTTP запросы.
### Функционал:
1. В случае успешной обработки сервис должен отвечать статусом 200, в случае любой ошибки — статус 400.
2. Сохранение всех объектов в базе данных.
3. Запросы:
- a. GET /city/ — получение всех городов из базы;
- b. GET /city//street/ — получение всех улиц города; (city_id —
идентификатор города)
- c. POST /shop/ — создание магазина; Данный метод получает json c
объектом магазина, в ответ возвращает id созданной записи.
- d. GET /shop/?street=&city=&open=0/1 — получение списка магазинов; 
> i. Метод принимает параметры для фильтрации. Параметры не обязательны. В случае отсутствия параметров выводятся все магазины, если хоть один параметр есть , то по нему выполняется фильтрация.

> ii. Важно!: в объекте каждого магазина выводится название города и улицы, а не id записей.

> iii. Параметр open: 0 - закрыт, 1 - открыт. Данный статус определяется исходя из параметров «Время открытия», «Время закрытия» и текущего времени сервера.

## Описание проекта:
Проект написан на языке Python с использованием библиотек: 
- DRF (Django Rest Framework)
- pcycorpg2
- pytest
- froozen_gun 

с использованием базы данных: PostgreSQL 

и добавлением Docker для более удобного запуска проекта.


## API

- #### GET /api/city - получает список всех городов из базы данных
> curl --location 'http://127.0.0.1:8000/api/city'

Возращает HTTP код 200 в случае успешного получения данных и тело ответа. Пример: [{ "id": 1, "name": "Gorod" }]

Возращает HTTP код 404 и сообщение 'Cities not created' в случае отсутствия городов в базе данных

- #### POST /api/city - создает новый объект города

> curl --location 'http://127.0.0.1:8000/api/city' \
--header 'Content-Type: application/json' \
--data '{ "name": "Gorod" }'

> Ожидает тело запроса. Пример:
`    { "name": "Gorod" }

Возращает HTTP код 201 в случае успешного создания объекта и тело ответа. Пример:{ "id": 1,"name": "Gorod"}

Возращает HTTP код 400 в случае некорректного запроса и тело ответа с описанием ошибки. Пример: {     "name": [         "This field is required."     ] }

Возращает HTTP код 400 в случае попытки записать город, именование которого уже есть в базе данных, и тело ответа с описанием ошибки. Пример: {     "name": [         "city with this name already exists."     ] }

- #### GET /api/street?city= - получает список всех улиц города по идентификатору города

> curl --location 'http://127.0.0.1:8000/api/shop?city=4'

city - обязательный параметр запроса

Возращает HTTP код 200 в случае успешного получения данных и тело ответа. Пример: [     {         "id": 1,         "name": "Street",         "city_id": "Gorod"     } ]

Возращает HTTP код 400 и сообщение 'City expected' в случае отсутствия параметра запроса city_id

- #### POST /api/street - создает новый объект улицы
> curl --location 'http://127.0.0.1:8000/api/street' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Street",
    "city": "Gorod"
}'

> Ожидает тело запроса. Пример:     {     "name" : "Street",     "city" : "Gorod" }

Также, создаст объект города по его названию, если в базе отстутсвует существующий город с таким же наименованием.

Возращает HTTP код 201 в случае успешного создания объекта и тело ответа. Пример: {         "id": 1,         "name" : "Street",         "city" : "Gorod"     }

Возращает HTTP код 400 в случае некорректного запроса и тело ответа с описанием ошибки. Пример: {     "name": [         "This field is required."     ],     "city": [         "This field is required."     ] }

- #### GET /api/shop?street=&city=&open= - получает список всех улиц города по идентификатору города

> curl --location 'http://127.0.0.1:8000/api/shop?street=2&city=4&open=1'

street, city, open - необязательные параметры запроса

| Query parameter |           Описание фильтра при указании           |
|-----------------|---------------------------------------------------|
| street          |В качестве значения передается идентификатор улицы. Возвращает все магазины на указанной улице.
| city            |В качестве значения передается идентификатор города. Возвращает все магазины в указанном городе.
| open            |В качестве значения передается 0 - флаг закрытия магазина и 1 - флаг открытия магазина. Возвращает либо список открытых магазинов относительно текущего времени, либо список закрытых магазинов. 

Возращает HTTP код 400 в случае некорректного запроса и тело ответа с описанием ошибки. 
Пример: {     "name": [         "This field is required."     ],     "street_id": [         "This field is required."     ],     "open_time": [         "This field is required."     ],     "close_time": [         "This field is required."     ],     "city": [         "This field is required."     ] }

- #### POST /api/shop

> curl --location 'http://127.0.0.1:8000/api/shop' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Magazin",
    "street": "Ulitsa",
    "city": "Gorod",
    "house": 131,
    "open_time": "10:00",
    "close_time": "22:00"
}'

> Ожидает тело запроса. Пример: {
    "name": "Magazin",
    "street": "Ulitsa",
    "city": "Gorod",
    "house": 131,
    "open_time": "10:00",
    "close_time": "22:00"
}

Также, создаст объект города и улицы по их названиям, если в базе отстутсвует существующие город и улица с такими же наименованиями.

Возращает HTTP код 201 в случае успешного создания объекта и id магазина.

Возвращает "Such data already exists", при попытке создания такого же объекта.
Не может быть создан объект магазина в том же городе, на той же улице и в том же доме.
## Запуск проекта в терминале локальной машины:

Для локального запуска проекта необходима существующая база данных.

Настройка подключения к БД настраивается в файле `shops/podrygomy/podrygomy/settings.py` в переменной **DATABASES** 

Для запуска проекта необходимо выполнить несколько комманд:

1. pip install virtualenv
2. virtualenv venv
3. venv\Scripts\activate
4. pip install django djangorestframework psycopg2
5. pip install pytest-django
6. cd podrygomy
7. python manage.py migrate
8. python manage.py runserver

## Запуск проекта в Docker-контейнере:

Для запуска проекта в Docker-контейнере необходим установленный и запущенный **Docker** на локальной машине.

Необходимо запустить терминал в директории shops/docker и выполнить команду:
`docker-compose up --build`

Подключиться к БД в контейнере Docker можно по следующим настройкам: 

- 'NAME': 'postgres'
- 'USER': 'postgres'
- 'PASSWORD': 'postgres'
- 'HOST': '127.0.0.1'
- 'PORT': '15432'

## Запуск unit-тестов:

Для локального запуска Unit-тестов, необходимо в терминале выполнить следующую команду:

- python manage.py test --verbosity 2