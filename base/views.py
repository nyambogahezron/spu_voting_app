from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from administration_app.models import Election, Position, RunningMate, Ballot
from .forms import UserForm, UserCreationForm_Customized
from django.db.models import Count


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
            # Check if the user has already voted for this position in this election
            user_has_voted = Ballot.objects.filter(user=request.user, position=position, election=election).exists()

            if not user_has_voted:
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



def vote(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        running_mate_id = request.POST.get('running_mate_id')
        election_id = request.POST.get('election_id')
        position_id = request.POST.get('position')

        user = User.objects.get(id=user_id)
        running_mate = RunningMate.objects.get(id=running_mate_id)
        election = Election.objects.get(id=election_id)
        position = Position.objects.get(id=position_id)

        ballot = Ballot.objects.filter(user=user, election=election, position=position)

        if ballot.exists():
            messages.error(request, 'You have already voted for this running mate in this election.')
        else:
            Ballot.objects.create(user=user, running_mate=running_mate, election=election,position=position)
            messages.success(request, 'Your vote has been recorded.')

    return redirect('home')


def results(request):
    # Get all elections
    elections = Election.objects.all()

    data = []

    for election in elections:
        election_data = {"name": election.name, "positions": []}

        # Get all positions for this election
        positions = Position.objects.filter(election=election)

        for position in positions:
            position_data = {"title": position.title, "running_mates": []}

            # Get all running mates for this position in this election
            running_mates = RunningMate.objects.filter(position=position, election=election)

            for running_mate in running_mates:
                # Get all ballots for this running mate in this election
                ballots = Ballot.objects.filter(running_mate=running_mate, election=election)

                # Get the total count of ballots
                total_count = ballots.count()

                position_data["running_mates"].append({"name": running_mate.name, "total_votes": total_count})

            # Sort running mates by total votes from largest to smallest
            position_data["running_mates"] = sorted(position_data["running_mates"], key=lambda rm: rm["total_votes"], reverse=True)

            election_data["positions"].append(position_data)

        data.append(election_data)

    return render(request, 'base/results.html', {"elections": data})



def logoutUser(request):
    logout(request)
    return redirect('home')
