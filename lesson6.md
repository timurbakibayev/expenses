**Удаление записей**

Меняем файл account.html, добавляем колонку для удаления записи:

    <table class="table table-hover">
    <thead>
        <tr>
            <th>id</th>
            <th>Описание</th>
            <th>Сумма</th>
            <th>Операции</th>
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
            <td><a class="btn btn-sm btn-danger" href="/delete/{{ transaction.id }}">delete</a></td>
        </tr>
    {% endfor %}
    </tbody>
    </table>

Мы добавили две строки:

    <th>Операции</th>
    и
    <td><a class="btn btn-sm btn-danger" href="/delete/{{ transaction.id }}">delete</a></td>

Теперь, если пользователь нажмёт на "удалить", его переведёт по ссылке "/delete/номер транзакции". 

Но Django не знает, что с этим делать, поэтому его необходимо проиструктировать:

**Что делать, когда прошли по /delete/transaction_id?**

Меняем urls.py, добавляем туда строку с /delete:

    urlpatterns = [
        path('', views.index, name='index'),
        path('admin/', admin.site.urls),
        path('register/', views_auth.registration, name='register'),
        path('login/', views_auth.login_view, name='login'),
        path('logout/', views_auth.logout_view, name='logout'),
        path('account/', views.account, name='account'),
        path('create/', views.create_view, name='create'),
        path('delete/<int:transaction_id>', views.delete_view, name='delete'),
    ]

Теперь Django будет пытаться запустить функцию delete_view в файле views.py. А этой функции у нас нет.
Поэтому добавляем её:

**Удаление записи из базы данных**

Добавляем функцию delete_view в файле views.py

    def delete_view(request: HttpRequest, transaction_id: int) -> HttpResponse:
        Transaction.objects.filter(id=transaction_id).filter(user=request.user).delete()
        return redirect("/")

Обратите внимание на filter(user=request.user), если не добавить эту часть, то любой пользователь
сможет удалить любую запись другого пользователя. А это не хорошо.

Попробуйте запустить проект и убедиться, что всё работает, как надо.

