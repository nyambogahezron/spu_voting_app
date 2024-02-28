from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from administration_app.models import Election, Position, RunningMate
from .forms import UserForm, UserCreationForm_Customized


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, email=email ,username=email , password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Invalid details")

    context = {}
    return render(request, 'base/login.html', context)


def registerUser(request):
    form = UserCreationForm_Customized()

    if request.method == 'POST':
        form = UserCreationForm_Customized(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "something went wrong!")
    context = {'form': form}

    return render(request, 'base/register.html', context)


def home(request):
    current_time = timezone.now()
    elections = Election.objects.filter(end_date__gt=current_time)
    data = []

    for election in elections:
        positions = Position.objects.filter(election=election)
        election_data = {
            'election': election,
            'positions': [],
        }
        for position in positions:
            running_mates = RunningMate.objects.filter(position=position, election=election)
            position_data = {
                'position': position,
                'running_mates': running_mates,
            }
            election_data['positions'].append(position_data)
        data.append(election_data)

    context = {
        'data': data,
    }
    return render(request, 'base/home.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')
