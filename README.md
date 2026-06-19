# Data Vault 2.0 Test Task

Тестовое задание на стажировку Data Engineer.

## Задача

Реализовать загрузку данных из REST API в корпоративное хранилище данных:

```text
Source → STG → DDS
```

Для моделирования слоя DDS используется методология **Data Vault 2.0**.

Источник данных:  
`https://jsonplaceholder.typicode.com/posts`

Бизнес-ключи:
- `id`
- `userId`

## Стек

- Python
- PostgreSQL
- Docker
- Data Vault 2.0

## Структура проекта

```text
.
├── ddl
│   ├── stg.sql
│   └── dds.sql
├── src
│   ├── config.py
│   ├── elt1.py
│   └── elt2.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Модель данных

### STG

Слой STG хранит данные из источника без бизнес-трансформаций.

Таблица:
- `stg.posts`

### DDS

DDS построен по Data Vault 2.0.

Таблицы:
- `dds.hub_user` — Hub для бизнес-ключа `userId`
- `dds.hub_post` — Hub для бизнес-ключа `id`
- `dds.link_user_post` — Link между пользователем и постом
- `dds.sat_post` — Satellite с описательными атрибутами поста: `title`, `body`

Для технических ключей используется MD5-хеширование.

## Запуск проекта

### 1. Запустить PostgreSQL

```bash
docker-compose up -d
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Создать таблицы

```bash
psql -h localhost -p 5432 -U postgres -d dv_db -f ddl/stg.sql
psql -h localhost -p 5432 -U postgres -d dv_db -f ddl/dds.sql
```

Пароль по умолчанию:

```text
postgres
```

### 4. Запустить ELT 1

Загрузка данных из REST API в STG:

```bash
python src/elt1.py
```

### 5. Запустить ELT 2

Перекладка данных из STG в DDS:

```bash
python src/elt2.py
```

## Результат

После выполнения скриптов данные будут загружены:

- в слой STG: `stg.posts`
- в слой DDS: `hub_user`, `hub_post`, `link_user_post`, `sat_post`
