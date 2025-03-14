from django.shortcuts import render, redirect
from Admin.models import Registration
from django.http import HttpResponse
from .models import GroundRegistration, Host_Tournament  # Corrected here
from hashlib import sha256
from django.views.decorators.cache import cache_control
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import datetime

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ground_reg(request, id):
    reg_ground = GroundRegistration.objects.all()  # Corrected here
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
        ob = GroundRegistration()  # Corrected here
        ob.uid = userid
        ob.ground_name = groundname
        ob.ground_location = location
        ob.ground_address = address
        ob.ground_desc = description
        ob.ground_feature = features
        ob.ground_rate = rate
        ob.ground_img = img
        if GroundRegistration.objects.filter(uid=user).exists():  # Corrected here
            return HttpResponse('Ground already exist!!')
        if GroundRegistration.objects.filter(ground_name=groundname).exists():  # Corrected here
            return HttpResponse('Ground name already exist!!')
        ob.is_available = 1
        ob.save()
        return redirect('index')
    else:
        return render(request, 'ground_reg.html', {'id': userid, 'dis': dis})

def tournament_reg(request, id):
    reg_ground = GroundRegistration.objects.filter(is_available=1)  # Corrected here
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
        ob.tournament_name = tournamentname  # Corrected here
        ob.tournament_date = tournamentdate  # Corrected here
        ob.tournament_desc = tournamentdescription  # Corrected here
        ob.tournament_rate = tournamentrate  # Corrected here
        if Host_Tournament.objects.filter(tournament_name=tournamentname).exists():  # Corrected here
            return HttpResponse('Tournament name already exist!!')
        ob.is_available = 1
        ob.save()
        return render(request, 'index.html', {'reg_ground': reg_ground, 'id': userid, 'dis': dis, 'reg_tournament': reg_tournament})
    else:
        return render(request, 'tournament_reg.html', {'id': userid, 'dis': dis})