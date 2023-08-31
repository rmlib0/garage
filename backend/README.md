# Garage.Backend

_"Garage" - backend part of garage project._
[![Docker](https://img.shields.io/badge/docker-24.0.2-blue.svg?logo=docker)](https://www.python.org/) [![Python](https://img.shields.io/badge/python-3.11-green.svg?logo=python)](https://www.python.org/) [![Django](https://img.shields.io/badge/django-4.1+-green.svg?logo=django)](https://www.djangoproject.com/) [![DRFW](https://img.shields.io/badge/django--rest--framework-3.12+-green.svg)](https://www.django-rest-framework.org/)


## Features
- Get statistics of sensors
- Switch status


## Tech
Production
[Docker][docker]

In backend main usage:
[Python][python]
[Django][django]
[DRFW][drfw]


## Template for .env
```
# Main settings
DEBUG=False
ALLOWED_HOSTS='example.com 127.0.0.1 localhost backend'
CSRF_TRUSTED_ORIGINS='https://example.com https://*.example.com'
SECRET_KEY=''

# Database settings
POSTGRES_DB=garage
POSTGRES_USER=garage
POSTGRES_PASSWORD=garage
DB_NAME=garage
DB_HOST=localhost
DB_PORT=5432
```


## Start project in Docker
Start docker compose
```
cd garage
sudo docker compose up
```
Make migrations
```
sudo docker compose exec backend python manage.py migrate
```
Superuser creation
```
sudo docker compose exec backend python manage.py createsuperuser
```
or change password for alredy existing superuser
```
sudo docker compose exec backend python manage.py changepassword admin
```
Collect static files
```
sudo docker compose exec backend python manage.py collectstatic
```
Copy to nginx staticfiles folder
```
sudo docker compose exec backend cp -r /app/static/. /app/static/
```


## API resouces and usage
List of endpoints.

| Resource                                | Allowed methods    |
| :-------------------------------------- | :----------------- |
| /api/                                   | GET                |
| /api/tags/                              | GET                |
| /api/tags/`tag_id`                      | GET                |
| /api/sensors/                           | GET, POST          |
| /api/recipes/`recipe_id`                | GET, PATCH, DELETE |
| /api/ingredients/                       | GET                |
| /api/ingredients/`ingredient_id`        | GET                |
| /api/recipes/download_shopping_cart/    | GET                |
| /api/recipes/`recipe_id`/shopping_cart/ | POST, DELETE       |
| /api/recipes/`recipe_id`/favorite/      | POST, DELETE       |
| /api/users/                             | GET, POST          |
| /api/users/`user_id`                    | GET                |
| /api/users/subscriptions/               | GET                |
| /api/users/`user_id`/subscribe/         | POST, DELETE       |
| /api/users/me/                          | GET                |
| /api/users/set_password/                | POST               |
| /api/auth/token/login/                  | POST               |
| /api/auth/token/logout/                 | POST               |


## Status Codes
Returns the following status codes in its API:

| Status Code | Description             |
| :---------- | :---------------------- |
| 200         | `OK`                    |
| 201         | `CREATED`               |
| 400         | `BAD REQUEST`           |
| 401         | `UNAUTHORIZED`          |
| 404         | `NOT FOUND`             |
| 500         | `INTERNAL SERVER ERROR` |


## Authors and resources
Mikhail Ovsjannikov <rmlib.null@gmail.com>  


## Greetings
Special greets to: 


## License
MIT
**Free Software, Hell Yeah!**

[docker]: https://www.docker.com/
[python]: https://www.python.org/
[django]: https://www.djangoproject.com/
[drfw]: https://www.django-rest-framework.org/
