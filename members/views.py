from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages


def login_user(request):
    context = {}
    return render(request, 'login.html', context)


def register_user(request):
    context = {}
    return render(request, 'register.html', context)
