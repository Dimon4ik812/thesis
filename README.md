# Сайт для бронирования столиков в ресторане

## Установка:
1. Клонировать репозиторий:

```
https://github.com/Dimon4ik812/thesis
```

2. Установка зависимостей:

```
poetry install
```

3. Задачи проекта:

```
На данном сайте размещена информация о ресторане. 
Есть возможность забронировать столик.
Существует панель администратора в нее входят: 
1. Просмотр и редактирование списка бронирований
2. Просмотр списка пользователя и блокировка их.
```

4. Запуск проекта локально: 

```
python manage.py runserver
```

## Контейнеризация с Docker

1. Убедитесь, что у Вас установлен Docker и Docker Compose.

2. Для сборки и запуска проекта в контейнерах выполните:
```
docker-compose up -d --build
```
3. Для остановки контейнеров выполните:
```
docker-compose down
```
## CI/CD с GitHub Actions

1. Убедитесь, что Ваш проект настроен для работы с GitHub Actions.

2. При каждом пуше в репозиторий будут запускаться тесты и линтинг кода, а также проверяться возможность сборки Docker-образов.

3. В случае успешных проверок проект будет автоматически развернут на удаленном сервере.

## Запуск проекта на удаленном сервере

1. Убедитесь, что сервер готов к работе с Docker и Docker Compose.

2. Настройте SSH-доступ к серверу для деплоя через GitHub Actions.

3. Проект будет автоматически разворачиваться на сервере при каждом успешном пуше в репозиторий.

4.  http://85.92.111.109/