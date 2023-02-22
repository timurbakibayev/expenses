Урок 1
======

**Создаем проект expenses**

Для этого создаем виртуальное окружение venv, устанавливаем django и выполняем команду

    django-admin startproject expenses

**Создаем приложение app**

    python manage.py startapp app

**Добавляем app в settings.py**

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'app',  # <-------- добавьте эту строку
    ]


**Настраиваем статики и скачиваем bootstrap**

В файле settings.py в разделе INSTALLED_APPS добавляем

    'django.contrib.staticfiles',

В файле urls.py добавляем

    from django.contrib import staticfiles
    urlpatterns += staticfiles.urlpatterns()

В папке проекта создаем папку static и в ней папку css, js, img

В папке проекта создаем папку templates и в ней папку app

В папке проекта создаем файл .gitignore и добавляем в него

    *.pyc
    __pycache__
    .DS_Store
    .env
    .idea
    db.sqlite3
    static

**Создаем базовый html файл, в котором будут все метаданные и bootstrap**

В папке templates создаем файл base.html и добавляем в него

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Expenses</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <div class="container">
            {% block content %}
            {% endblock %}
        </div>
    </body>
    </html>

**Создаем страничку приветствия**

В папке templates/app создаем файл index.html и добавляем в него

    {% extends 'base.html' %}
    {% block content %}
        <h1>Expenses</h1>
    {% endblock %}
