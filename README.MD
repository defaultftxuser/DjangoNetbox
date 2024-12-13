# 🚀 Упрощенный аналог сервиса NetBox на Django

## 📜 Описание

Простое веб-приложение для управления серверным оборудованием, использующее Django и Django REST Framework.  
Приложение включает модели **DeviceModel**, **Device**, интеграцию с сервисом [DaData](https://dadata.ru/) для автодополнения и CRUD-операции с API и админкой.

---

## 🛠️ Технологии

- **Python 3.10+**
- **Django**: Основной фреймворк
- **Django REST Framework (DRF)**: Для создания REST API
- **DaData API**: Интеграция для автозаполнения адресов
- **TokenAuthentication**: Для авторизации пользователей по токену

---

## 💻 Установка

1. Клонируйте репозиторий:

## Запуск
### Docker
#### Прокинуть зависимости
#### дев версия
> docker-compose -f docker_compose/dev/compose_dev.yaml --env-file .env up --build

