**Делаем формочку для создания новой записи**

Создаём файл create.html:

    {% extends 'base.html' %}
    {% block content %}
    <h1>Новая запись</h1>
    <form action="" method="post" style="max-width: 800px">
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
        <input class="btn btn-info" type="submit" value="Добавить">
    </form>
    {% endblock %}

Создаём обработчик формы create.html в файле views.py:

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
    
        return render(request, "create.html")

Здесь мы проверяем, авторизован ли пользователь. Если нет, то перенаправляем его на главную страницу. 
Если пользователь авторизован, то создаём новую запись в базе данных. 
После этого перенаправляем пользователя на главную страницу.

Когда создаём запись, смотрим, доход это или расход. 
Если доход, то сумма записывается как есть.
Если расход, то сумма записывается со знаком минус.

**Добавляем ссылку на создание новой записи**

Добавляем ссылку на создание новой записи в файл account.html:

    <a class="btn btn-info" href="/create">Добавить</a>

И, соответственно отображаем её в urls.py

    path('create/', views.create_view, name='create'),

Попробуйте теперь создать расходы и доходы. 
Попробуйте зайти под другим пользователем и убедиться, что у каждого свои записи.

