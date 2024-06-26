# Your Bookkeeping

## ToDo
1. [X] Реализовать возможность редактировать справочники
2. [X] Реализовать возможность удаления записей из справочника
3. [X] Добавить локализацию en, ru
4. [ ] Реализовать регистрацию
5. [ ] Добавить список проектов пользователя (CRUD)
6. [ ] Добавить список пользователей в проекте (CRUD)
7. [X] Добавить в фильтр Account категорию все
8. [ ] Сделать документацию пользователя
9. [ ] Добавить пагинацию для списка транзакций
10. [X] Добавить в справочник категории тип категории (Расход, Доход)
11. [ ] Добавить страницу обратная связь
12. [ ] Добавить инструкцию для каждого действия (Добавить расход, добавить доход) с разбивкой по шагам
13. [ ] Добавить возможность вести бухгалтерию в нескольких проектах
14. [ ] Добавить возможность прикреплять изображение для расхода
15. [X] Исправить редирект после добавления записи в справочник
16. [ ] Добавлять список шаблонных категорий при регистрации

## Run
```commandline
python manage.py runserver
```

## Migrate
```commandline
python manage.py migrate
```

```commandline
python manage.py makemigrations transactions
python manage.py sqlmigrate transactions 0004
```

## Create Super User
```commandline
python manage.py createsuperuser
```

## LoadData
```commandline
python manage.py loaddata transactions/transaction_type_reference.json
```

## New Secret Key
```commandline
python manage.py shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"
```

## Update prod
```commandline
git fetch origin main
git merge origin main
```

## Build localize file
```commandline
python .\manage.py makemessages -l ru -i .venv
python .\manage.py compilemessages
```
