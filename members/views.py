from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from members.forms import CreateUserForm, ChangeUserForm
from members.models import Subscription
from recipes.models import MenuCategory, Allergy, MealType


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
            user = form.save()
            login(request, user)
            update_session_auth_hash(request, user)
            return redirect('profile')

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
    subscription = Subscription.objects.filter(user=request.user).first()
    if subscription:
        allergies = ', '.join([str(allergy) for allergy in subscription.allergies.all()])
        num_meals = subscription.meals.count()
    else:
        subscription = None
        allergies = None
        num_meals = None

    context = {
        'form': form,
        'subscription': subscription,
        'allergies': allergies,
        'num_meals': num_meals,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
@transaction.atomic
def subscription(request):
    if request.method == 'GET':
        if Subscription.objects.filter(user=request.user, paid=True).first():
            return redirect('profile')

    if request.method == 'POST':
        for i in request.POST.items():
            print(i)
        subscription = Subscription()
        subscription.user = request.user
        subscription.duration = request.POST.get('duration')
        subscription.person_count = request.POST.get('person_count')
        foodtype = request.POST.get('foodtype')

        if foodtype == 'low':
            subscription.menu_category = MenuCategory.objects.get(title='Vegan')
        elif foodtype == 'veg':
            subscription.menu_category = MenuCategory.objects.get(title='Lowcarb')
        elif foodtype == 'keto':
            subscription.menu_category = MenuCategory.objects.get(title='Keto')
        else:
            subscription.menu_category = MenuCategory.objects.get(title='Classic')
        subscription.save()

        if int(request.POST.get('breakfast')) == 0:
            subscription.meals.add(MealType.objects.get(label__iexact='breakfast'))
        if int(request.POST.get('lunch')) == 0:
            subscription.meals.add(MealType.objects.get(label__iexact='lunch'))
        if int(request.POST.get('dinner')) == 0:
            subscription.meals.add(MealType.objects.get(label__iexact='dinner'))
        if int(request.POST.get('dessert')) == 0:
            subscription.meals.add(MealType.objects.get(label__iexact='dessert'))

        for key, value in request.POST.items():
            if key.startswith('allergy'):
                subscription.allergies.add(Allergy.objects.get(id=int(value)))

        return redirect('profile')

    context = {'allergies': Allergy.objects.all()}
    return render(request, 'order.html', context)
