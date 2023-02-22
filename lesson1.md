Урок 1
======

**Создаем проект expenses**

Для этого создаем виртуальное окружение venv, устанавливаем django и выполняем команду

    django-admin startproject expenses .

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

В файле settings.py в разделе STATIC_URL добавляем

    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR / 'static'

В файле urls.py добавляем

    from django.conf.urls.static import static
    from expenses import settings
    urlpatterns += += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

В папке приложения app создаем папку app/static.
Скачиваем bootstrap из getbootstrap.com -> docs -> downloads и копируем в папку app/static папки css и js.

**Создаем базовый html файл, в котором будут все метаданные и bootstrap**

В файле settings.py в разделе TEMPLATES добавляем 'templates' в DIRS

    'DIRS': ['templates'],

В папке app создаем папку templates, внутри неё создаем файл base.html и добавляем в него

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

В папке app/templates создаем файл index.html и добавляем в него

    {% extends 'base.html' %}
    {% block content %}
        <h1>Expenses</h1>
    {% endblock %}

В файле app/views.py добавляем
    
    from django.shortcuts import render
    from django.http import HttpRequest, HttpResponse
    
    
    def index(request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html')

В файле app/urls.py добавляем

    from app import views
    ...    
    urlpatterns = [
        ...
        path('', views.index, name="index"),
        ...
    ]

**Итоговая структура дерева папок**

    expenses
    ├── app
    │   ├── migrations
    │   ├── static
    │   │   ├── css
    │   │   └── js
    │   ├── templates
    │   │   ├── base.html
    │   │   └── index.html
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── expenses
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── manage.py
