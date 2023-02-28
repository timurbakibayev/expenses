from django.shortcuts import render, redirect

from app.models import Transaction


def index(request):
    if request.user.is_authenticated:
        return redirect('/account')
    else:
        return render(request, 'index.html')


def account(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    transactions = Transaction.objects.filter(user=user)

    return render(request, 'account.html', {'user': user, "transactions": transactions})
