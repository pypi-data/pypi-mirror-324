Django management command to run WSGI server for production. Also support serving static files through WhiteNoise.

## Usage
Install it from PyPI:-

```
uv add django-runprod
```

Add it to `INSTALLED_APPS`:-

```
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_runprod",
    ...
]
```

Run it through management command:-

```
python manage.py runprod
```

## License
MIT
