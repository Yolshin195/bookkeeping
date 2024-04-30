# Your Bookkeeping

## ToDo
1. [ ] Реализовать возможность редактировать справочники
2. [ ] Реализовать возможность удаления записей из справочника
3. [ ] Добавить локализацию en, ru
4. [ ] Реализовать регистрацию
5. [ ] Добавить список проектов пользователя (CRUD)
6. [ ] Добавить список пользователей в проекте (CRUD)
7. [ ] Добавить в фильтр Account категорию все
8. [ ] Сделать документацию пользователя

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
