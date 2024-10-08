# City REST API

## Описание

Этот проект представляет собой HTTP API для управления информацией о городах. Основные функции включают:

- Добавление и удаление городов из хранилища.
- Запрос информации о городах.
- Поиск двух ближайших городов по заданным координатам (широте и долготе).

## Стек технологий

- **Django**: Веб-фреймворк для создания API и управления данными.
- **Django REST Framework (DRF)**: Для построения RESTful API.
- **PostgreSQL**: Реляционная база данных для хранения информации о городах.
- **Docker**: Для контейнеризации приложения и базы данных.
- **docker-compose**: Для управления многоконтейнерными приложениями.
- **graphhopper**: Сторонее API для получения координат (широты и долготы). 

## Установка и запуск

1. **Клонирование репозитория**

```bash
$ git clone https://github.com/B-smalls/taskCDN
$ cd taskCDN
```
2. **Настройка .env**
```bash
$ mv .env.dev .env
```
Пример .env:
```bash
$ SECRET_KEY='your-secret-key-here'
$
$ DEBUG=True
$ ALLOWED_HOSTS="127.0.0.1,localhost"
$
$ PG_DATABASE=your_database_name
$ PG_USER=your_database_user
$ PG_PASSWORD=your_database_password
$ DB_HOST=localhost
$ DB_PORT=5432
$
$ API_KEY="your-api-key-here"
```

3. **Получение API ключа**
Регистрация:
```c
https://www.graphhopper.com/
```

4. **Docker**

Запуск: 

```bash
$ docker-compose up --build
```

Остановка:
```bash
$ docker-compose down
```

## Описание методов API

Базовый URL: 
```c
http://<HOST>:<PORT>
```

Значения `HOST` и `PORT` устанавливаются в `.env` файле.

Заголовки в каждом запросе:
```c
'Content-Type: application/json'
```

### Добавление города

- **Метод:** `POST`
- **Эндпоинт:** `/api/coordinatesCity/createCity/`
- **Описание:** Добавляет новый город в хранилище по его названию. Координаты города автоматически запрашиваются из внешнего API.
- **Параметры запроса:**
  - **Тело запроса (JSON):**
    ```json
    {
      "cityName": "Название города"
    }
    ```
#### Пример успешного ответа

- **Статус:** `201 Created`
- **Тело ответа (JSON):**
```json
{
    "id": 1,
    "cityName": "New York",
    "latitude": 40.7128,
    "longitude": -74.0060
}
```

#### Возможные ошибки
Пример ответа с ошибкой:
- **Статус:** `400 Bad Request`
- **Тело ответа (JSON):**
```json
{
  "error": "Failed to create city."
}
```

| Код | Описание                                              |
| --- | ----------------------------------------------------- |
| 500 | Ошибка на стороне сервера.                            |
| 400 | Ошибка в переданных данных.                           |
| 404 | Пользователь не найден.                               |

---

### Удаление города

- **Метод:** `DELETE`
- **Эндпоинт:** `/api/coordinatesCity/deleteCity/<str:cityName>/`
- **Описание:** Удаляет город из хранилища по его названию.
- **Параметры запроса:**
  - **URL параметр:**
    - `cityName`: Название города для удаления.

#### Пример успешного ответа
- **Код:** `204 No Content`
- **Описание:** Если город успешно удален.

#### Возможные ошибки
- **Код:** `404 Not Found`
- **Описание:** Если город не найден в хранилище.

---

### Получение информации о городе

- **Метод:** `GET`
- **Эндпоинт:** `/api/coordinatesCity/getCity/<str:cityName>/`
- **Описание:** Запрашивает информацию о городе по его названию.

#### Параметры запроса

- **URL параметр:**
  - `cityName`: Название города для получения информации.

#### Пример успешного ответа

```json
{
    "id": 1,
    "cityName": "New York",
    "latitude": 40.7128,
    "longitude": -74.0060
}
```
#### Возможные ошибки
Пример ответа с ошибкой:
- **Статус:** `404 Not Found`
- **Тело ответа (JSON):**
```json
{
  "error": "City with name 'Ujeev' not found."
}
```

---

### Получение всех городов

- **Метод:** `GET`
- **Эндпоинт:** `/api/coordinatesCity/getAllCity/`
- **Описание:** Получает информацию обо всех городах в хранилище.

#### Пример успешного ответа

```json
    [
      {
        "id": 1,
        "cityName": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060
      },
      {
        "id": 2,
        "cityName": "Los Angeles",
        "latitude": 34.0522,
        "longitude": -118.2437
      }
    ]
```

---

### Поиск ближайших городов

- **Метод:** `POST`
- **Эндпоинт:** `/api/coordinatesCity/nearCity/`
- **Описание:** Находит два ближайших города по заданным широте и долготе.

- **Параметры запроса:**

  - **Тело запроса (JSON):**

```json
    {
      "latitude": 40.730610,
      "longitude": -73.935242
    }
```

#### Пример успешного ответа

- **Статус:** `200 Ok`
- **Тело ответа (JSON):**
```json
{
  "nearest_city_1": "Москва",
  "nearest_city_2": "Санкт-Петербург"
}
```

#### Возможные ошибки
Пример ответа с ошибкой:
- **Статус:** `400 Bad Request`
- **Тело ответа (JSON):**
```json
{
  "error": "JSON parse error - Expecting value: line 2 column 15 (char 16)"
}
```

Пример ответа с ошибкой:
- **Статус:** `400 Bad Request`
- **Тело ответа (JSON):**
```json
{
  "error": "Failed to find nearest cities."
}
```

## Описание таблицы базы данных

### Таблица `City`

Таблица `City` хранит информацию о городах. Структура таблицы следующая:

| Поле         | Тип данных   | Описание                      |
|--------------|--------------|-------------------------------|
| `id`          | `INTEGER`    | Уникальный идентификатор города (автоинкремент). |
| `cityName`    | `VARCHAR(100)`| Название города.               |
| `latitude`    | `FLOAT`      | Широта города.                 |
| `longitude`   | `FLOAT`      | Долгота города.                |

### Примеры данных

| id | cityName     | latitude | longitude |
|----|--------------|----------|-----------|
| 1  | Moscow        | 55.7558   | 37.6176    |
| 2  | New York      | 40.7128   | -74.0060   |
| 3  | Tokyo         | 35.6895   | 139.6917   |

**Примечания:**
- Поле `id` является автоматически создаваемым уникальным идентификатором для каждого города.
- Поле `cityName` содержит название города, которое должно быть уникальным.
- Поля `latitude` и `longitude` представляют координаты города и хранятся в формате с плавающей запятой.

