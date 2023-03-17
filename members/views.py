from django.shortcuts import redirect, render
from members.forms import CreateUserForm, ChangeUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
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
    form = ChangeUserForm(instance=request.user)
    if request.method == 'POST':
        form = ChangeUserForm(request.POST, instance=request.user)
        form_data = form.data.copy()
        form_data['email'] = request.user.email

        form.data = form_data

        if form.is_valid():
            user = form.save()
            if password := form.cleaned_data.get('password1'):
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
            messages.info(request, 'Data has been changed')
            return redirect('profile')
    context = {'form': form}
    return render(request, 'profile.html', context)
