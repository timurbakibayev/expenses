from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect('/account')
    else:
        return render(request, 'index.html')


def account(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")
    return render(request, 'account.html', {'user': user})
