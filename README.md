
# feedbacker_for_art api_final
## Авторы:
[kultmet](https://github.com/kultmet)

[serebrennikovalexander](https://github.com/serebrennikovalexander)

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
Выполнить загрузку информации в базу данных:

```
python manage.py fill_database
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
{
  "name": "string",
  "slug": "string"
}
```

## Требования:
```
asgiref==3.5.2
atomicwrites==1.4.1
attrs==22.1.0
certifi==2022.9.24
charset-normalizer==2.0.12
colorama==0.4.5
Django==2.2.16
django-filter==21.1
djangorestframework==3.12.4
djangorestframework-simplejwt==5.2.1
idna==3.4
importlib-metadata==4.13.0
iniconfig==1.1.1
packaging==21.3
pluggy==0.13.1
py==1.11.0
PyJWT==2.1.0
pyparsing==3.0.9
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
pytz==2022.4
requests==2.26.0
sqlparse==0.4.3
toml==0.10.2
typing_extensions==4.3.0
urllib3==1.26.12
zipp==3.8.1
```
