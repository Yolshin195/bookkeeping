# Your Bookkeeping

## Run
```commandline
python manage.py runserver
```

## Migrate
```commandline
python manage.py migrate
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
