### Dershop Backend
Dershop Backend is online shop web application to help the shop owner deliver their own online shopping website.
The feature is manage product, order, customer, etc.

### Technology
* Django
* Django Rest Framework

### Formatter/Linter
```commandline
black .
```

### Installation
```commandline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Run Server
```commandline
source .venv/bin/activate
python manage.py runserver
```