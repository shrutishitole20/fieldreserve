from django.shortcuts import render, redirect
from Admin.models import Registration
from django.http import HttpResponse
from .models import GroundRegistration, Host_Tournament
from django.views.decorators.cache import cache_control
from django.contrib import messages
import datetime

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ground_reg(request, id):
    reg_ground = GroundRegistration.objects.all()
    reg_tournament = Host_Tournament.objects.all()
    dis = Registration.objects.get(id=id)
    user = dis.id
    userid = request.session['id']
    if request.method == 'POST':
        groundname = request.POST.get('groundname')
        location = request.POST.get('location')
        address = request.POST.get('address')
        description = request.POST.get('description')
        features = request.POST.get('feat')
        rate = request.POST.get('rate')
        img = request.FILES['image']
        ob = GroundRegistration()
        ob.uid = userid
        ob.ground_name = groundname
        ob.ground_location = location
        ob.ground_address = address
        ob.ground_desc = description
        ob.ground_feature = features
        ob.ground_rate = rate
        ob.ground_img = img
        if GroundRegistration.objects.filter(uid=user).exists():
            return HttpResponse('Ground already exist!!')
        if GroundRegistration.objects.filter(ground_name=groundname).exists():
            return HttpResponse('Ground name already exist!!')
        ob.is_available = 1
        ob.save()
        return redirect('index')
    else:
        return render(request, 'ground_reg.html', {'id': userid, 'dis': dis})

def tournament_reg(request, id):
    reg_ground = GroundRegistration.objects.filter(is_available=1)
    reg_tournament = Host_Tournament.objects.filter(is_available=1)
    dis = Registration.objects.get(id=id)
    userid = request.session['id']
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        tournamentname = request.POST.get('tournamentname')
        tournamentdate = request.POST.get('tournamentdate')
        tournamentdescription = request.POST.get('tournamentdescription')
        tournamentrate = request.POST.get('tournamentrate')
        if tournamentdate < today:
            return HttpResponse('Select an Upcoming Date')
        ob = Host_Tournament()
        ob.uid = userid
        ob.tournament_name = tournamentname
        ob.tournament_date = tournamentdate
        ob.tournament_desc = tournamentdescription
        ob.tournament_rate = tournamentrate
        if Host_Tournament.objects.filter(tournament_name=tournamentname).exists():
            return HttpResponse('Tournament name already exist!!')
        ob.is_available = 1
        ob.save()
        return render(request, 'index.html', {'reg_ground': reg_ground, 'id': userid, 'dis': dis, 'reg_tournament': reg_tournament})
    else:
        return render(request, 'tournament_reg.html', {'id': userid, 'dis': dis})

def index(request):
    reg_ground = GroundRegistration.objects.filter(is_available=1)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    reg_tournament = Host_Tournament.objects.filter(is_available=1)

    # Filter grounds by type
    football_grounds = GroundRegistration.objects.filter(ground_type='Football', is_available=1)
    volleyball_grounds = GroundRegistration.objects.filter(ground_type='Volleyball', is_available=1)
    cricket_grounds = GroundRegistration.objects.filter(ground_type='Cricket', is_available=1)
    badminton_grounds = GroundRegistration.objects.filter(ground_type='Badminton', is_available=1)
    tennis_grounds = GroundRegistration.objects.filter(ground_type='Tennis', is_available=1)

    if 'id' in request.session:
        user_id = request.session['id']
        request.session['id'] = user_id
        dis = Registration.objects.get(id=user_id)
        return render(request, 'index.html', {
            'id': user_id,
            'dis': dis,
            'reg_ground': reg_ground,
            'reg_tournament': reg_tournament,
            'football_grounds': football_grounds,
            'volleyball_grounds': volleyball_grounds,
            'cricket_grounds': cricket_grounds,
            'badminton_grounds': badminton_grounds,
            'tennis_grounds': tennis_grounds,
        })
    else:
        return render(request, 'index.html', {
            'reg_ground': reg_ground,
            'reg_tournament': reg_tournament,
            'football_grounds': football_grounds,
            'volleyball_grounds': volleyball_grounds,
            'cricket_grounds': cricket_grounds,
            'badminton_grounds': badminton_grounds,
            'tennis_grounds': tennis_grounds,
        })

def success_view(request):
    return render(request, 'success.html')

def host_tournament_view(request):
    return HttpResponse("Host Tournament View")