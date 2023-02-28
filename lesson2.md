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
          <input name="password2" type="password" class="form-control" id="password2" placeholder="confirm password">
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

Создаем обработчик формы регистрации, который будет проверять введенные данные 
и выводить сообщение об ошибке, если данные не прошли валидацию.

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
                    user = authenticate(username=email, password=password)
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

Создаем обработчик формы авторизации, который будет проверять введенные данные 
и выводить сообщение об ошибке, если данные не прошли валидацию.

Редактируем файл views_auth.py и добавляем в него обработчик формы авторизации и выхода.

    from django.contrib.auth import authenticate, login, logout
    from django.shortcuts import render, redirect
    
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

    def logout_view(request):
        logout(request)
        return redirect("/")


**Создаем страничку личного кабинета**

Если пользователь не авторизован, то показываем общую информацию о проекте. 

Для этого редактируем index.html файл:

    {% extends 'base.html' %}
    {% block content %}
    <h1>Главная страница</h1>
    <p>Добро пожаловать на сайт!</p>
    <p>Чтобы зарегистрироваться, нажмите <a href="/register">сюда</a></p>
    <p>Чтобы авторизоваться, нажмите <a href="/login">сюда</a></p>
    {% endblock %}

Если пользователь авторизован, то показываем информацию 
о нём (redirect на страницу личного кабинета).

Для этого редактируем функцию index в файле views.py:

    from django.shortcuts import render, redirect
    
    def index(request):
        if request.user.is_authenticated:
            return redirect('/account')
        else:
            return render(request, 'index.html')

Создаём файл account.html и добавляем в него информацию о пользователе.

    {% extends 'base.html' %}
    {% block content %}
    <h1>Личный кабинет</h1>
    <p>Добро пожаловать, {{ user.first_name }}!</p>
    <p>Ваш email: {{ user.email }}</p>
    <p><a href="/logout">Выйти</a></p>
    {% endblock %}

Добавляем функцию account в файле views.py:

    from django.shortcuts import render
    
    def account(request):
        user = request.user
        return render(request, 'account.html', {'user': user})

**Изменяем urls.py**

Изменяем urls.py, чтобы при переходе на главную страницу сайта, 
если пользователь не зарегистрирован, то показывалась общая информация о проекте, 
а если пользователь зарегистрирован, то показывалась информация о нём.

    from app import views_auth
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.index, name='index'),
        path('register/', views_auth.registration, name='register'),
        path('login/', views_auth.login_view, name='login'),
        path('logout/', views_auth.logout_view, name='logout'),
        path('account/', views.account, name='account'),
    ]


**Миграция данных**

Чтобы проект нормально работал, нам уже нужна база данных с таблицами пользователя. 
Так как эта таблица стандартная в Django, всё, что нам необходимо сделать, это

    python manage.py migrate

Можно запускать проект, проверьте, что работают:

- Регистрация
- Выход
- Авторизация
- Обработчик ошибок при неправильной регистрации и авторизации
- Личный кабинет
