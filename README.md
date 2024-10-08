## Сервис управления процессами на складе.
`Приложение для управления процессами на складе. Приложение создано на фреймворке FastAPI.
В качестве базы данных применен асинхронный движок PostgreSQL, интегрированный с ORM SQLAlchemy версии 2, 
что обеспечивает высокую производительность и удобство работы с данными. 
Миграции базы данных автоматизируются с помощью инструмента Alembic,` 

`Для обеспечения надежного мониторинга и записи операций использован модуль logger для логирования. 
В дополнение к этому, приложение включает автотесты, разработанные с использованием библиотеки pytest. 
Автотесты запускаются в изолированной среде в памяти, не влияя на основную базу данных с помошью асинхроннй базы данных sqlite+aiosqlite`

## Основной стек приложения

* FastAPI
* SQLAlchemy
* PostgreSQL
* alembic
* pytest
* logger

## Архитектура приложения

![architecture.jpg](app/architecture.jpg)

## Клонирование проекта

1. Клонируйте репозиторий:

```bash
git clone https://github.com/VladiFinogenov/FastAPI-Warehouse-Management-Service.git
```

2. Создайте и активируйте виртуальную среду:

| Операция \ ОС |           Windows            |               Linux / macOS |
|:--------------|:----------------------------:|----------------------------:|
| Создание      |     python -m venv .venv     |       python3 -m venv .venv |
| Активация     | .\.venv\Scripts\activate.bat | source ./.venv/bin/activate |
| Деактивация   |          deactivate          |               deactivate    |

## Настройки переменных окружения

`Создайте файл или проверьте что он там есть .env.docker в директории c настройками config.py и добавьте в него переменные окружения:`

```
# Замените настройки для БД на свои
POSTGRES_USER = 'postgres_user'
POSTGRES_PASSWORD = 'postgres_password'
POSTGRES_SERVER = 'db' # или 'localhost' без докер сборки,
POSTGRES_PORT = 5432
POSTGRES_DB = 'postgres_database'
```
`! Убедитесь, что sqlalchemy.url в файле alembic.ini соответствует параметрам переменных окружения`

## Сборка проекта через Docker compose

### Шаг 1: Запустите билд контейнеров.

`В корнеой директории приложения запустите команду в консоли`

```bash
docker compose up -d --build
````

### Шаг 2: Запуск миграций

```bash
docker compose exec web alembic upgrade head
````

`Дополнительно можно проверить в консоли что таблицы созданы командой:`

```bash
docker compose exec db psql --username=postgres_user --dbname=postgres_database

\l
````

## Работа с базой данных

`Документация по подключению БД через SQLAlchemy`

https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls

## Создание пользователя для PostgreSQL на linux

<details>

### Шаг 1: Установка PostgreSQL (если еще не установлено)

`Данная инструкция не предусмотрена текущей документацией`

### Шаг 2: Вход в систему PostgreSQL

1. **Переключитесь на пользователя `postgres`:**
   PostgreSQL устанавливает специального пользователя с именем `postgres`, который имеет право управлять БД.

```bash
sudo -i -u postgres
````

2. **Запустите консоль psql:**

```bash
psql
````
### Шаг 3: Создание пользователя

Для создания нового пользователя выполните следующую команду в консоли `psql`:

`
CREATE USER имя_пользователя WITH PASSWORD 'ваш_пароль';
`
#### Пример:
```sql
CREATE USER postgres_user WITH PASSWORD 'postgres_password';
```
#### Ожидаемый результат:

`CREATE ROLE`

### Шаг 4: Создание БД и передача прав созданному пользователю

Для создания БД выполните следующую команду в консоли `psql`:

`
CREATE DATABASE имя_БД OWNER имя_пользователя ENCODING 'UTF8';
`
#### Пример:
```sql
CREATE DATABASE postgres_database OWNER postgres_user ENCODING 'UTF8';
```
#### Ожидаемый результат:

`CREATE DATABASE`

### Заключение

`Вы успешно создали нового пользователя и базу данных в PostgreSQL на Linux`

`Для выхода из консоли PostgreSQL используйте команду:`

```bash
\q
````
в терминале IDE Pycharm
```bash
exit
````
</details>

## Создание миграций

<details>

### Шаг 1: создание среды миграции для асинхронной поддержки

Для создания среды миграции выполните команду:
```bash
alembic init -t async app/migrations
````
### Шаг2: Изменить настройки alembic.ini

* Измените опцию sqlalchemy.url в файле alembic.ini на URL подключения к БД:

sqlalchemy.url = postgresql+asyncpg://имя_пользователя:пароль@localhost:5432/имя_БД

`На основе предложенного .env файла:`

sqlalchemy.url = postgresql+asyncpg://postgres_user:postgres_password@db:5432/postgres_database

* Изменить настройки env.py target_metadata = None на:

```
from app.core.backend.db import Base
from app.data.models import *

target_metadata = Base.metadata
```

* Выполнить первую миграцию командой

```bash
alembic revision --autogenerate -m "Initial migration"
```

* Выполнить команду: "alembic upgrade head" - применение самой последней созданной миграции
`Эта команда запустит все миграции, которые еще не были применены к вашей базе данных, начиная с последней созданной миграции.`

### основные команды в Alembic:

* alembic upgrade +2 две версии включая текущую для апгрейда
* alembic downgrade -1 на предыдущую для даунгрейда
* alembic current получить информацию о текущей версии
* alembic history --verbose история миграций, более подробнее можно почитать в документации.
* alembic downgrade base даунгрейд в самое начало миграций
* alembic upgrade head применение самой последней созданной миграции

</details>

## Запуск приложения локально 

`
uvicorn app.main:app --port 8000 --reload
`

## Документация Swagger

http://127.0.0.1:8000/docs/ 

## Запуск тестов

<details>

* запустите в консоли команду

```bash
pytest
```

* Запуск тестов с отчетом о покрытии % кода

`Установите библиотеку pytest-cov`

```bash
pip install pytest-cov
```

`Запустите тесты командой:`

```bash
pytest --cov=app --cov-report=term-missing
```

</details>

## Pre-commit 

<details>

`установите библиотеки в виртуальное окружение`

pip install pre-commit

pip install isort

* Установка хуков pre-commit

pre-commit install

** Примечания: 

`Убедитесь, что версии `pre-commit` и `isort`, которые вы используете, совместимы друг с другом.`

pre-commit autoupdate

* Запустите `pre-commit`

pre-commit run --all-files

</details>

## Логирование 

`настройки логирования находятся /FastAPI-WMS/app/core/logging_config.py`

`автоматически записываются в файл app.log в корне проекта`