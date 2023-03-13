**Удаление записей с подтверждением**

Меняем файл account.html, заменяем ссылку <a> на кнопку <button> и сообщаем браузеру,
что в случае нажатия на кнопку необходимо запустить функцию delete_transaction.

Чуть ниже в этом же файле описываем функцию delete_transaction в теге <script>.

Должен получиться такой файл:

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
                <td><button class="btn btn-sm btn-danger" onclick="delete_transaction({{ transaction.id }})">delete</button></td>
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
    
    {% endblock %}

Вот и всё, теперь, если пользователь нажмёт на удаление записи, браузер сначала спросит, уверен ли он.

