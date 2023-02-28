**Создаём суперпользователя**

    $ python manage.py createsuperuser

Обязательно укажите емэйл в качестве имени пользователя и, собственно, емэйла. 
Т.е. email придётся написать дважды.

**Создаём модель transaction**

В файле models.py добавляем модель Transaction

    from django.db import models
    from django.contrib.auth.models import User
    
    
    class Transaction(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        created = models.DateField(auto_now_add=True)
        modified = models.DateField(auto_now=True)
        description = models.CharField(max_length=10_000, blank=True, null=True)
        amount = models.IntegerField(default=0)
    
        def __str__(self):
            return f"{self.description}: {self.amount} KZT"

Не забудьте выполнить миграцию

    $ python manage.py makemigrations
    $ python manage.py migrate

И добавить модель в admin.py

    from django.contrib import admin
    from .models import Transaction
    
    
    admin.site.register(Transaction)

**Отображаем транзакции**

Для этого сначала создаём таблицу внутри account.html:

    {% extends 'base.html' %}
    {% block content %}
    <h1>Личный кабинет</h1>
    <p>Добро пожаловать, {{ user.first_name }}!</p>
    <p>Ваш email: {{ user.email }}</p>
    <p><a href="/logout">Выйти</a></p>
    
    <h2>Транзакции</h2>
        <table class="table table-hover">
        <thead>
            <tr>
                <th>id</th>
                <th>Описание</th>
                <th>Сумма</th>
            </tr>
        </thead>
        <tbody>
        {% for transaction in transactions %}
            <tr>
                <td>{{ transaction.id }}</td>
                <td>{{ transaction.description }}</td>
                <td style="color: {% if transaction.amount < 0 %}red{% else %}darkgreen{% endif %}">
                    {{ transaction.amount }} KZT
                </td>
            </tr>
        {% endfor %}
        </tbody>
        </table>
    {% endblock %}

И изменяем функцию account в views.py

    def account(request):
        user = request.user
        if not user.is_authenticated:
            return redirect("/")
    
        transactions = Transaction.objects.filter(user=user)
    
        return render(request, 'account.html', {'user': user, "transactions": transactions})

**Добавляем транзакции через админку**

В админке добавляем транзакции, чтобы проверить, что всё работает.
