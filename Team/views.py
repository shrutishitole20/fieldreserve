from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from Admin.models import Registration
from Organizer.models import GroundRegistration, Host_Match
from .models import Match_Booking, Ground_Booking, Rating,Rating
from hashlib import sha256
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import datetime
import uuid
from django.conf import settings


# Existing views...

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
        ob.mid = Match_details.id  # Use the correct field name 'mid'
        ob.Match_name = Match_details
        ob.ground_id = reg.id
        if Match_Booking.objects.filter(uid=dis.id, mid=Match_details.id).exists():  # Use the correct field name 'mid'
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
            request.session['booking_id'] = ob.id
            return redirect('payment_page')
        else:
            return render(request, 'ground_booking.html', {'ground_details': ground_details})
    else:
        return HttpResponse('Need To Login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rate(request, id):
    ground_details = GroundRegistration.objects.get(id=id)
    if 'id' in request.session:
        user_id = request.session['id']
        dis = Registration.objects.get(id=user_id)
        if request.method == 'POST':
            star = request.POST.get('star')
            if not star:
                return HttpResponse('Rating value is required', status=400)
            ob = Rating(
                uid=user_id,
                user_name=dis,
                Ground_name=ground_details.ground_name,
                ground_id=ground_details.id,
                star=star
            )
            if Rating.objects.filter(uid=user_id, ground_id=ground_details.id).exists():
                Rating.objects.filter(uid=user_id, ground_id=ground_details.id).update(star=star)
                return HttpResponse('Rating updated')
            ob.save()
            return HttpResponse('Rating given')
        return redirect('about')
    return HttpResponse('User not logged in', status=401)

# New reservation and payment views...

def reservation_form(request):
    """View to display the initial reservation form"""
    form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form})

def payment_page(request):
    if 'booking_id' in request.session:
        booking_id = request.session['booking_id']
        booking = Ground_Booking.objects.get(id=booking_id)
        ground = GroundRegistration.objects.get(id=booking.ground_id)
        amount = ground.ground_rate 
        return render(request, 'payment_page.html', {'booking': booking, 'amount': amount})
    else:
        return HttpResponse('No booking found')
