**Редактирование записей**

Нам необходимо для начала создать очень много модальных окон - для каждой транзакции по окну.

Для этого создаём файл edit.html, который очень похож на create.html:

    <div class="modal fade" id="modal_edit_{{ transaction.id }}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Редактировать запись</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
            <form action="/edit/{{ transaction.id }}" method="post" style="max-width: 800px">
              <div class="modal-body">
                    {% csrf_token %}
                    <div class="mb-3">
                      <label for="description" class="form-label">Описание</label>
                      <input name="description" value="{{ transaction.description }}" type="text" class="form-control" id="description" required>
                    </div>
                    <div class="mb-3">
                      <label for="amount" class="form-label">Сумма</label>
                      <input value="{{ transaction.amount_abs }}" name="amount" type="number" class="form-control" id="amount">
                    </div>
                    <div class="mb-3">
                      <label for="type" class="form-label">Тип</label>
                        <select name="type" id="type" class="form-control">
                            <option value="expense" {% if transaction.amount < 0 %}selected{% endif %}>Расход</option>
                            <option value="income" {% if transaction.amount > 0 %}selected{% endif %}>Доход</option>
                        </select>
                    </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                <button type="submit" class="btn btn-primary">Сохранить</button>
              </div>
            </form>
        </div>
      </div>
    </div>

Здесь можно заметить использование transaction.amount_abs, которого нет в природе.

Давайте это исправим, добавим функцию amount_abs в модели transaction:

    class Transaction(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        created = models.DateField(auto_now_add=True)
        modified = models.DateField(auto_now=True)
        description = models.CharField(max_length=10_000, blank=True, null=True)
        amount = models.IntegerField(default=0)
    
        def __str__(self):
            return f"{self.description}: {self.amount} KZT"
    
        def amount_abs(self) -> int:
            return abs(self.amount)


**Добавляем модальные окна в account.html**

Меняем файл account.html: для каждой транзакции добавляем кнопку редактирования
и в конце файла добавляем модальные окна для каждой транзакции:

Должен получиться такой уже довольно большой файл:

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
                <td>
                    <button class="btn btn-sm btn-danger" onclick="delete_transaction({{ transaction.id }})">удалить</button>
                    <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#modal_edit_{{ transaction.id }}">ред</button>
                </td>
            </tr>
        {% endfor %}
        </tbody>
        </table>
    
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
          Добавить
        </button>
    
        <script>
            const delete_transaction = (transaction_id) => {
                const result = confirm("Удалить транзакцию номер " + transaction_id + "?");
                if (result === true) {
                    const url = "/delete/"+transaction_id;
                    window.location = url;
                }
            }
        </script>
    
    {% include "create.html" %}
    
    {% for transaction in transactions %}
        {% include "edit.html" %}
    {% endfor %}
    
    {% endblock %}

Здесь необходимо обратить внимание на эту строку:

    <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#modal_edit_{{ transaction.id }}">ред</button>

В ней мы используем такой же идентификатор, как и в edit.html (самая первая строка):

    data-bs-target="#modal_edit_{{ transaction.id }}"

Это для того, чтобы для каждой транзакции вызывалось своё модальное окно.

**Добавляем редактирование транзакций**

Теперь нам нужно добавить функционал редактирования транзакций (файл views.py):

    def edit_view(request: HttpRequest, transaction_id: int) -> HttpResponse:
        transaction = Transaction.objects.filter(id=transaction_id).filter(user=request.user).first()
    
        if request.method == "POST":
            transaction.description = request.POST.get("description", "")
            if request.POST.get("type", "") == "expense":
                transaction.amount = -abs(int(request.POST.get("amount", 0)))
            if request.POST.get("type", "") == "income":
                transaction.amount = abs(int(request.POST.get("amount", 0)))
            transaction.save()
            return redirect("/")
    
        raise NotImplementedError

Здесь мы получаем транзакцию по id, проверяем, что она принадлежит пользователю, и если всё ок, то обновляем её.

**Добавляем путь для редактирования транзакций**

Добавляем путь в файл urls.py:

    path('edit/<int:transaction_id>', views.edit_view, name='edit'),

Должен получиться в итоге такой файл:

    from django.contrib import admin
    from django.urls import path
    from django.conf.urls.static import static
    from expenses import settings
    from app import views, views_auth
    
    urlpatterns = [
        path('', views.index, name='index'),
        path('admin/', admin.site.urls),
        path('register/', views_auth.registration, name='register'),
        path('login/', views_auth.login_view, name='login'),
        path('logout/', views_auth.logout_view, name='logout'),
        path('account/', views.account, name='account'),
        path('create/', views.create_view, name='create'),
        path('delete/<int:transaction_id>', views.delete_view, name='delete'),
        path('edit/<int:transaction_id>', views.edit_view, name='edit'),
    ]
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

Вот и всё! Теперь можно редактировать транзакции.
