from django.shortcuts import redirect, render
from members.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_user(request):
    next_url = request.GET.get("next", '/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            messages.info(request, 'Email or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def register_user(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    context = {}
    return render(request, 'profile.html', context)
