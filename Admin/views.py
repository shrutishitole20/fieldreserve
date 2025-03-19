from django.shortcuts import render, redirect
from django.http import HttpResponse
from Admin.models import Registration
from Organizer.models import GroundRegistration, Host_Tournament
from Team.models import Tournament_Booking, Ground_Booking
from django.views.decorators.cache import cache_control
from django.db.models import Q
from django.contrib import messages
import datetime

# Create your views here.

def index(request):
    reg_ground = GroundRegistration.objects.filter(is_available=1)  
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    reg_tournament = Host_Tournament.objects.filter(is_available=1) 
    if 'id' in request.session:
        user_id = request.session['id']
        request.session['id'] = user_id
        dis = Registration.objects.get(id=user_id)
        return render(request, 'index.html', {'id': user_id, 'dis': dis, 'reg_ground': reg_ground, 'reg_tournament': reg_tournament}) 
    else:  
        return render(request, 'index.html', {'reg_ground': reg_ground, 'reg_tournament': reg_tournament})

def reg(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        mail = request.POST.get('email')
        pwd = request.POST.get('password')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        ob = Registration()
        ob.user_name = uname
        ob.user_email = mail
        ob.user_pass = pwd
        ob.user_phone = phone
        ob.role = role
        if Registration.objects.filter(user_name = uname).exists():
            return HttpResponse('User name already exist!!')
        ob.status = 0
        ob.save()
        return redirect('login')
    else:
        return redirect('login')

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Registration.objects.filter(user_name = username, user_pass = password).exists():
            user_details = Registration.objects.get(user_name = username, user_pass = password)
            user_id = user_details.id
            request.session['id'] = user_id
            return redirect('index')
        else:
            return HttpResponse('wrong user name or password or account does not exist!!')
    return render(request, 'login.html')

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def lgout(request):
    request.session.flush()
    return redirect('index')

def about(request, id):
    details = GroundRegistration.objects.get(id = id)
    if 'id' in request.session:
        user_id = request.session['id']
        dis = Registration.objects.get(id = user_id)
        return render(request, 'about.html', {'id': user_id, 'details': details, 'dis': dis})
    else:
        return render(request, 'about.html', {'details': details})

def tournament_about(request, id):
    if Host_Tournament.objects.filter(id = id, is_available = 1).exists():
        reg_tournament = Host_Tournament.objects.get(id = id)
        reg_user = reg_tournament.uid
        ground_details = GroundRegistration.objects.get(uid = reg_user)
        if 'id' in request.session:
            user_id = request.session['id']
            dis = Registration.objects.get(id = user_id)
            reg_dis = Registration.objects.get(id = reg_user)
            return render(request, 'tournament_about.html', {'id': user_id, 'dis': dis, 'reg_tournament': reg_tournament, 'ground_details': ground_details, 'reg_dis': reg_dis})
        else:
            return render(request, 'tournament_about.html', {'reg_tournament': reg_tournament, 'ground_details': ground_details})
    else:
        return HttpResponse('Tournament not available')

def profile(request):
    user_id = request.session['id']
    dis = Registration.objects.get(id=user_id)
    if 'organizer' in dis.role:
        ground_details = GroundRegistration.objects.get(uid=user_id,is_available=1)
        reg_tournament=Host_Tournament.objects.filter(uid=user_id,is_available=1)
        m=ground_details.id
        book_tournament=Tournament_Booking.objects.filter(ground_id=m)
        reg_ground=Ground_Booking.objects.filter(ground_id=ground_details.id,is_available=1)
        return render(request,'profile.html', {'id': user_id,'dis':dis,'reg_tournament':reg_tournament,'ground_details':ground_details,'book_tournament':book_tournament,'reg_ground':reg_ground})
    elif 'team' in dis.role:
        reg_tournament=Host_Tournament.objects.filter(is_available=1)
        book_tournament=Tournament_Booking.objects.filter(uid=dis.id)
        result = []
        for i in book_tournament:
            rt=Host_Tournament.objects.get(id=i.tid)
            result.append(rt)
        reg_ground=Ground_Booking.objects.filter(uid=user_id)
        return render(request,'profile.html', {'id': user_id,'dis':dis,'book_tournament':book_tournament,'reg_tournament':reg_tournament,'result':result,'reg_ground':reg_ground})
def search(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        msg=" "
        reg_ground = GroundRegistration.objects.filter(ground_location=data,is_available=1)
        reg_tournament=Host_Tournament.objects.filter(tournament_name=data,is_available=1)
        if(GroundRegistration.objects.filter(ground_location=data,is_available=1)).exists():
            reg_ground = GroundRegistration.objects.filter(ground_location=data,is_available=1)
        elif(GroundRegistration.objects.filter(ground_name=data,is_available=1)).exists():
            reg_ground = GroundRegistration.objects.filter(ground_name=data,is_available=1)
        elif(Host_Tournament.objects.filter(tournament_name=data,is_available=1)).exists():
            reg_tournament=Host_Tournament.objects.filter(tournament_name=data,is_available=1)
        else:
            msg = " Result not found "
        
        if 'id' in request.session:
            user_id = request.session['id']
            request.session['id'] = user_id
            dis = Registration.objects.get(id=user_id)
            if msg == " ":
                return render(request, 'search.html',{'id': user_id,'dis':dis,'reg_ground': reg_ground,'reg_tournament':reg_tournament})
            else:
                return render(request, 'search.html',{'id': user_id,'dis':dis,'reg_ground': reg_ground,'reg_tournament':reg_tournament,'msg':msg}) 

def cancel(request, id):
    userid = request.session['id']
    dis = Registration.objects.get(id = userid)
    if 'organizer' in dis.role:
        Host_Tournament.objects.filter(is_available = 1, id = id).update(is_available = 0)
        return redirect('profile')
    elif 'team' in dis.role:
        if Tournament_Booking.objects.filter(id = id).exists():
            Tournament_Booking.objects.filter(id = id).delete()
        elif Ground_Booking.objects.filter(id = id, is_available = 1).exists():
            Ground_Booking.objects.filter(id = id, is_available = 1).delete()
        return redirect('profile')