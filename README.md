# PhotoApp

## Краткое описание проекта
PhotoApp - учебный проект, состоящий из fullstack Django-приложения и RESTful API к нему, написанному с помощью `django-rest-framework`.  
Приложение представляет из себя платформу для фотоконкурса/фотовыставки, где пользователи делятся фотографиями, которые другие пользователи могут комментировать и лайкать. На сайте присутствует модерация фотографий, а также система нотификаций в реальном времени.

## Используемый ЯП
Python 3.13.3

## Используемые БД
PostgreSQL 16.4.1  
Redis 7.2.5

## Перечень используемых пакетов
- django-split-settings
- python-decouple
- django-viewflow
- factory-boy
- python-social-auth
- django-imagekit
- celery
- channels
- django-rest-framework
- Django
- psycopg2
- social-auth-app-django
- redis
- [django-service-objects]("https://git.snpdev.ru/saltpepper/django-service-objects.git")
- django-extensions
- pyparsing
- pydot
- pre-commit
- daphne
- channels-redis
- django-log-request-id
- rich
- aiosmtpd
- djangorestframework-simplejwt["crypto"]
- drf-spectacular
- djangorestframework-api-key
- [service-objects-autodocs]("https://git.snpdev.ru/saltpepper/service-objects-autodocs")

## Установка локально
Чтобы установить локально, склонируйте репозиторий с помощью:
```bash
git clone https://github.com/bibrikthesorcerer/photo_app.git
```
Затем, установите следующие программные зависимости проекта с помощью пакетного менеджера:
- Python
- Poetry
- PostgreSQL
- Redis
- Celery

## Запуск локально
1. Установите зависимости проекта с помощью:
```bash
poetry install
```
2. Запустите Celery для работы с отложенными задачами:
```bash
celery -A conf worker -l INFO
```
3. Запустите проект:
```bash
python manage.py runserver
```

### OAuth
В проекте настроен логин и регистрация через OAuth GitHub. Для его работы необходимо зарегистрировать приложение на https://github.com/settings/developers, во вкладке OAuth Apps. Полученные Client ID и Secret Key необходимо ввести в `.env`.

### Почтовый клиент
Сайт использует почту пользователей для отправки писем при сбросе пароля и добавлению пароля к аккаунтам, созданным с помощью OAuth. Этот функционал требует создания почтового ящика и заполнения значений в секции Email файла `.env`. 

## Документация API
Документация к RESTful API находится на `localhost:8000/api/schema/swagger-ui/`

## Список сервисов и программ, необходимых для работы и настройки окружения приложения на серверах
- Python
- Poetry
- PostgreSQL
- Redis
- Celery
- Почтовый клиент, необходимый для работы сброса пароля на сайте