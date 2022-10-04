# api_final
## Авторы:
[kultmet](https://github.com/kultmet)
[??](https://github.com/??)
[olka-ayacaste](https://github.com/olka-ayacaste)
## Описание:
### REST API для YaMDb
Создан на основе библиотеки [Django REST Framework (DRF)](https://github.com/ilyachch/django-rest-framework-rusdoc)


>YaMDb - это платформа для сбора отзывов и оценок по различным категориям.

## Технологии
Python 3.7

Django 3.2.15


## Запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:kultmet/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

>Когда вы запустите проект, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация для API YaMDb. В документации описано, как работает API. Документация представлена в формате Redoc.

## Примеры запросов

* Основные эндпоинты для аутентификации нового пользователя
> Для аутентификации применены JWT-токены.

  Создание JWT-токена:
```
http://127.0.0.1:8000/api/v1/jwt/create/
```
> Токен необходимо передавать в заголовке каждого запроса, в поле Authorization. Перед самим токеном должно стоять ключевое слово Bearer и пробел.

* Основные эндпоинты API
```
http://127.0.0.1:8000/api/v1/categories/
```
```
http://127.0.0.1:8000/api/v1/genres/
```
```
http://127.0.0.1:8000/api/v1/titles/
```
> пример POST запроса на (http://127.0.0.1:8000/api/v1/categories/):
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
