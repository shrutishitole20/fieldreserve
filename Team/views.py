from django.shortcuts import render, redirect
from django.http import HttpResponse
from Admin.models import Registration
from Organizer.models import GroundRegistration, Host_Match
from .models import Match_Booking, Ground_Booking, rating
from hashlib import sha256
from django.views.decorators.cache import cache_control
from django.db.models import Q
from django.contrib import messages
import datetime

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def match_booking(request, id):
    Match_details = Host_Match.objects.get(id=id)
    m = Match_details.uid
    user_id = request.session['id']
    dis = Registration.objects.get(id=user_id)
    reg = GroundRegistration.objects.get(uid=m)
    if request.method == 'POST':
        ob = Match_Booking()
        ob.uid = user_id
        ob.user_name = dis
        ob.tid = Match_details.id
        ob.Match_name = Match_details
        ob.ground_id = reg.id
        if Match_Booking.objects.filter(uid=dis.id, tid=Match_details.id).exists():
            return HttpResponse('Already Booked For This Match')
        else:
            ob.save()
            return HttpResponse('Match Booked')
    else:
        return HttpResponse('Something went wrong!...')

def ground_booking_details(request, id):
    ground_details = GroundRegistration.objects.get(id=id)
    if 'id' in request.session:
        user_id = request.session['id']
        dis = Registration.objects.get(id=user_id)
        time_slot = Ground_Booking.objects.filter()
        return render(request, 'ground_book.html', {'id': user_id, 'dis': dis, 'ground_details': ground_details, 'time_slot': time_slot})
    else:
        return HttpResponse('You need to login to Book!')

def ground_booking(request, id):
    ground_details = GroundRegistration.objects.get(id=id)
    groundid = ground_details.id
    if 'id' in request.session:
        user_id = request.session['id']
        dis = Registration.objects.get(id=user_id)
        if request.method == 'POST':
            ob = Ground_Booking()
            st = request.POST.get('start_time')
            et = request.POST.get('end_time')
            dt = request.POST.get('ground_date')
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            if st == '':
                return HttpResponse('All fields need to be filled!')
            elif et == '':
                return HttpResponse('All fields need to be filled!')
            elif dt == '':
                return HttpResponse('All fields need to be filled!')
            elif dt < today:
                return HttpResponse('Select another date')
            ob.uid = user_id
            ob.user_name = dis
            ob.Ground_name = ground_details
            ob.ground_id = ground_details.id
            if Ground_Booking.objects.filter(date=dt, start_time=st, end_time=et, ground_id=groundid).exists():
                return HttpResponse('Time is not available')
            ob.date = dt
            ob.start_time = st
            ob.end_time = et
            ob.is_available = 1
            ob.save()
            return HttpResponse('Ground is Booked')
    else:
        return HttpResponse('Need To Login')

def rate(request, id):
    ground_details = GroundRegistration.objects.get(id=id)
    groundid = ground_details.id
    if 'id' in request.session:
        user_id = request.session['id']
        dis = Registration.objects.get(id=user_id)
        if request.method == 'POST':
            ob = rating()
            star = request.POST.get('rate')
            ob.uid = user_id
            ob.user_name = dis
            ob.Ground_name = ground_details.ground_name
            ob.ground_id = ground_details.id
            ob.star = star
            if rating.objects.filter(uid=user_id, ground_id=ground_details.id).exists():
                rating.objects.filter(uid=user_id, ground_id=ground_details.id).update(star=star)
                return HttpResponse('Rating updated')
            ob.save()
            return HttpResponse('Rating given')
        return redirect('about')