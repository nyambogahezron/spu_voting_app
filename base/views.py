from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import UserForm, UserCreationForm_Customized


def loginUser(request):

    context = {}
    return render(request, 'base/login.html', context)


def registerUser(request):

    context = {}
    return render(request, 'base/register.html', context)


def home(request):

    return render(request, 'base/home.html')


def logoutUser(request):
    logout(request)
    return redirect('home')
