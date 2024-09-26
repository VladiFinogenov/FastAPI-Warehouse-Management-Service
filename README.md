# Сервис управления процессами на складе.
`Приложение для управления процессами на складе. Приложение создано на фреймворке FastAPI. 
Использован асинхронный движок БД PostgreSQL под управлением ОРМ SQLAlchemy V2 и автоматизацией миграций alembic.`

## Основной стек приложения

* fastapi==0.115.0
* jinja2==3.1.4
* SQLAlchemy==2.0.35
* PostgreSQL



## Запуск приложения

`
uvicorn app.main:app --port 8000 --reload
`

## Настройка переменных окружения

`Создайте файл .env в корневой директории проекта и добавьте в него переменные окружения:`

```
# Замените настройки для БД на свои 
POSTGRES_USER = 'postgres_wms'
POSTGRES_PASSWORD = 'secure_password'
POSTGRES_SERVER = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DB = 'postgres_wms'
```

<details>
<summary># Работа с базой данных  </summary>

`Документация по подключению БД через SQLAlchemy`

https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls

## Создание пользователя для PostgreSQL на linux

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
CREATE USER postgres_wms WITH PASSWORD 'postgres_wms';
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
CREATE DATABASE postgres_wms OWNER postgres_wms ENCODING 'UTF8';
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
## Создание миграций

### Шаг 1: создание среды миграции для асинхронной поддержки

Для создания среды миграции выполните команду:
```bash
alembic init -t async app/migrations
````
### Шаг2: Изменить настройки alembic.ini

* Измените опцию sqlalchemy.url в файле alembic.ini на URL подключения к БД: 

sqlalchemy.url = postgresql+asyncpg://имя_пользователя:пароль@localhost:5432/имя_БД

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