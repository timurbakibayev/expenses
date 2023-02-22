Урок 2
======

**Создаем форму регистрации**

Создаем HTML форму регистрации с полями:

* Email
* Имя
* Пароль
* Подтверждение пароля

Создаём html файл registration.html и добавляем в него форму регистрации.

    {% extends 'base.html' %}
    {% block content %}
    <h1>Регистрация</h1>
    <form action="" method="post">
        {% csrf_token %}
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input name="email" type="email" class="form-control" id="email" placeholder="name@example.com" required>
        </div>
        <div class="mb-3">
          <label for="username" class="form-label">Имя</label>
          <input name="username" type="text" class="form-control" id="username" placeholder="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input name="password" type="password" class="form-control" id="password" placeholder="password">
        </div>
        <div class="mb-3">
          <label for="password2" class="form-label">Confirm password</label>
          <input type="password" class="form-control" id="password2" placeholder="confirm password">
        </div>
        {% if message %}
        <div class="alert alert-danger" role="alert">
          {{ message }}
        </div>
        {% endif %}
        <input type="submit" value="Зарегистрироваться">
    </form>
    {% endblock %}

**Создаем обработчик формы регистрации**

Создаем обработчик формы регистрации, который будет проверять введенные данные и выводить сообщение об ошибке, если данные не прошли валидацию.

Создаём файл views_auth.py и добавляем в него обработчик формы регистрации.

    from django.shortcuts import render
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate, login
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    
    def registration(request):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if User.objects.filter(username=email).exists():
                message = 'Пользователь с таким Email уже существует'
                return render(request, 'registration.html', {'message': message})
            if password == password2:
                try: 
                    user = User.objects.create_user(username=email, password=password)
                    user.first_name = username
                    user.save()
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect("/")
                except:
                    message = 'Ошибка регистрации'
                    return render(request, 'registration.html', {'message': message})
            else:
                message = 'Пароли не совпадают'
                return render(request, 'registration.html', {'message': message})
        else:
            return render(request, 'registration.html')

**Создаем форму авторизации**

Создаем HTML форму авторизации с полями:

* Email
* Пароль

Создаём html файл login.html и добавляем в него форму авторизации.

    {% extends 'base.html' %}
    {% block content %}
    <h1>Авторизация</h1>
    <form action="" method="post">
        {% csrf_token %}
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input name="email" type="email" class="form-control" id="email" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input name="password" type="password" class="form-control" id="password">
        </div>
        {% if message %}
        <div class="alert alert-danger" role="alert">
          {{ message }} 
        </div>
        {% endif %}
        <input type="submit" value="Войти">
    </form>
    {% endblock %}

**Создаем обработчик формы авторизации**

Создаем обработчик формы авторизации, который будет проверять введенные данные и выводить сообщение об ошибке, если данные не прошли валидацию.

Редактируем файл views_auth.py и добавляем в него обработчик формы авторизации.

    from django.contrib.auth import authenticate, login
    
    def login_view(request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                message = 'Неверный логин или пароль'
                return render(request, 'login.html', {'message': message})
        else:
            return render(request, 'login.html')


**Создаем страничку личного кабинета**

Если пользователь не зарегистрирован, то показываем общую информацию о проекте. 

Для этого создаём простой index.html файл:

    {% extends 'base.html' %}
    {% block content %}
    <h1>Главная страница</h1>
    <p>Добро пожаловать на сайт!</p>
    <p>Чтобы зарегистрироваться, нажмите <a href="/register">сюда</a></p>
    <p>Чтобы авторизоваться, нажмите <a href="/login">сюда</a></p>
    {% endblock %}

Если пользователь зарегистрирован, то показываем информацию о нём.

Создаём файл account.html и добавляем в него информацию о пользователе.

    {% extends 'base.html' %}
    {% block content %}
    <h1>Личный кабинет</h1>
    <p>Добро пожаловать, {{ user.first_name }}!</p>
    <p>Ваш email: {{ user.email }}</p>
    {% endblock %}


