**Делаем модальное окно для создания новой записи**

Меняем файл create.html (исходники один в один скопированы с getbootstrap.com):

    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Добавить запись</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
            <form action="/create/" method="post" style="max-width: 800px">
              <div class="modal-body">
                    {% csrf_token %}
                    <div class="mb-3">
                      <label for="description" class="form-label">Описание</label>
                      <input name="description" type="text" class="form-control" id="description" required>
                    </div>
                    <div class="mb-3">
                      <label for="amount" class="form-label">Сумма</label>
                      <input name="amount" type="number" class="form-control" id="amount">
                    </div>
                    <div class="mb-3">
                      <label for="type" class="form-label">Тип</label>
                        <select name="type" id="type" class="form-control">
                            <option value="expense">Расход</option>
                            <option value="income">Доход</option>
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

Обратите внимание на строку номер 8: action="/create/"

Идея в том, что, несмотря на то, что мы находимся сейчас в /account, форму мы по прежнему
хотим отправить в /create/.

**Добавляем эту форму в account.html**

Вот так должен выглядеть новый account.html

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
    
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
          Добавить
        </button>
    
    {% include "create.html" %}
    
    {% endblock %}

Обратите внимание на последние строки:

- изменили кнопку Добавить 
- включили "create.html", где хранитс наше модальное окно)

**Добавляем JS от Bootstrap в base.html**

Теперь base.html выглядит так:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Expenses</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    {#    <link rel="stylesheet" href="/static/css/style.css">#}
    </head>
    <body>
        <div class="container">
            {% block content %}
            {% endblock %}
        </div>
        <script src="/static/js/bootstrap.min.js"></script>
    </body>
    </html>

Здесь добавилась строка "script src = bootstrap".

**Убираем GET запрос из пути /create**

Раньше мы могли зайти в /create и заполнить там форму. Сейчас там модальное окно, а значит, 
никакой страницы там нет (там часть страницы только). 

Это значит, что если пришёл GET запрос, то его нужно отклонить:

    def create_view(request):
        user = request.user
        if not user.is_authenticated:
            return redirect("/")
    
        if request.method == "POST":
            if request.POST.get("type", "") == "expense":
                Transaction.objects.create(
                    user=user,
                    description=request.POST.get("description", ""),
                    amount=-abs(int(request.POST.get("amount", 0))),
                )
            if request.POST.get("type", "") == "income":
                Transaction.objects.create(
                    user=user,
                    description=request.POST.get("description", ""),
                    amount=abs(int(request.POST.get("amount", 0))),
                )
            return redirect("/")
    
        raise NotImplementedError

Здесь поменялась только последняя строка.

Всё готово, поздравляю! Можно пробовать добавлять новые записи!
