# Bank App

Это Django-приложение для управления кошельками, которое позволяет:
- Создавать кошельки.
- Пополнять и списывать средства с кошельков.
- Получать текущий баланс кошелька.

Приложение разработано с использованием следующих технологий:
**Backend**: Django (Python 3.12) + Django REST Framework  
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/Django%20REST-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)


**База данных**: PostgreSQL  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

**Очередь задач**: Celery + Redis  
[![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryproject.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

**Веб-сервер**: Nginx + Gunicorn  
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)

**Контейнеризация**: Docker + Docker Compose  
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)

**GitHub Actions**  
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

---

## Техническое задание

### Требования
1. **API**:
   - `POST /api/v1/wallets/<WALLET_UUID>/operation` — выполнение операций (пополнение или списание).
   - `GET /api/v1/wallets/<WALLET_UUID>` — получение баланса кошелька.
2. **Конкурентная обработка**:
   - Приложение должно корректно обрабатывать 1000 RPS на один кошелек.
3. **Обработка ошибок**:
   - Возвращать корректные HTTP-статусы и сообщения об ошибках (например, недостаточно средств, неверный JSON).
4. **Docker**:
   - Приложение и база данных должны запускаться в Docker-контейнерах.
   - Конфигурация должна настраиваться через переменные окружения.
5. **Тестирование**:
   - Эндпоинты должны быть покрыты тестами.

---

## Установка и запуск

### 1. Клонирование репозитория
```bash
  git clone hhttps://github.com/scorp5438/bank.git
  cd bank
```

### 2. Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте в него следующие переменные:

    DJANGO_SECRET_KEY=ваш-секретный-ключ
    DJANGO_DEBUG=True
    DJANGO_DB_NAME=
    DJANGO_DB_USERNAME=
    DJANGO_DB_PASSWORD=
    DJANGO_DB_HOST=
    DJANGO_DB_PORT=

### 3. Запуск с помощью Docker Compose

```bash
  docker-compose up --build
```
После запуска приложение будет доступно по адресу:


    Nginx: http://localhost:81/

### 4. API Endpoints
#### 4.1. Получить баланс кошелька
**Метод: GET**

    URL: /api/v1/wallets/<WALLET_UUID>/

**Пример ответа**:

    {
      "id": "1",
      "balance": "1000.00"
    }
#### 4.2. Выполнить операцию с кошельком
**Метод: PATCH**

    URL: /api/v1/wallets/<WALLET_UUID>/operation/

**Тело запроса:**

    {
      "operationType": "DEPOSIT",
      "amount": 100
    }
**Пример ответа:**

    {
      "message": "wallet balance 1 successfully changed. Current balance 1100.00"
    }

### Запуск тестов в GitHub Actions
    Тесты автоматически запускаются при пуше в ветку dev-branch.
    Результаты тестирования можно посмотреть в разделе Actions на GitHub.
