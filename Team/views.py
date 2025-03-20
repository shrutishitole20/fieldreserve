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
            return HttpResponse('Ground is Booked')
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

@csrf_exempt
def process_reservation(request):
    """Process the reservation form and prepare payment details"""
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Save reservation data temporarily but don't commit
            reservation = form.save(commit=False)
            
            # Generate a unique transaction ID
            transaction_id = str(uuid.uuid4())[:12]
            request.session['transaction_id'] = transaction_id
            
            # Store form data in session for later use
            request.session['reservation_data'] = {
                'full_name': form.cleaned_data['full_name'],
                'contact_number': form.cleaned_data['contact_number'],
                'email': form.cleaned_data['email'],
                'date': form.cleaned_data['date'].strftime('%d-%m-%Y'),
                'time_slot': form.cleaned_data['time_slot'],
                'amount': 4500,  # Set your amount here or calculate based on form data
            }
            
            # Redirect to payment page
            return redirect('payment_page')
        else:
            return render(request, 'reservation_form.html', {'form': form})
    
    return redirect('reservation_form')

def payment_page(request):
    """Display the payment options (UPI)"""
    # Get reservation data from session
    reservation_data = request.session.get('reservation_data', {})
    
    # Set payment expiration time (30 minutes from now)
    expiry_time = (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime('%H:%M')
    
    context = {
        'reservation_data': reservation_data,
        'expiry_time': expiry_time,
        'transaction_id': request.session.get('transaction_id', '')
    }
    
    return render(request, 'payment_page.html', context)

@csrf_exempt
def verify_payment(request):
    """Verify payment status and finalize the reservation"""
    if request.method == 'POST':
        payment_status = request.POST.get('payment_status')
        transaction_id = request.session.get('transaction_id')
        
        if payment_status == 'success' and transaction_id:
            # Get reservation data from session
            reservation_data = request.session.get('reservation_data', {})
            
            # Create and save the reservation
            reservation = Reservation(
                full_name=reservation_data.get('full_name'),
                contact_number=reservation_data.get('contact_number'),
                email=reservation_data.get('email'),
                date=datetime.datetime.strptime(reservation_data.get('date'), '%d-%m-%Y').date(),
                time_slot=reservation_data.get('time_slot'),
                transaction_id=transaction_id,
                payment_status='Completed',
                amount_paid=reservation_data.get('amount')
            )
            reservation.save()
            
            # Clear session data
            if 'reservation_data' in request.session:
                del request.session['reservation_data']
            if 'transaction_id' in request.session:
                del request.session['transaction_id']
            
            return JsonResponse({'status': 'success', 'redirect_url': '/confirmation/'})
        
        return JsonResponse({'status': 'failed', 'message': 'Payment verification failed'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def payment_confirmation(request):
    """Display payment confirmation page"""
    return render(request, 'confirmation.html')