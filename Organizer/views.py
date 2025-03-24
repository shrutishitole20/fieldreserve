from django.shortcuts import render, redirect
from Admin.models import Registration
from django.http import HttpResponse, JsonResponse
from .models import GroundRegistration, Host_Match
from django.views.decorators.cache import cache_control
from django.contrib import messages
import datetime
import json
import requests
import hashlib
from django.conf import settings
from .forms import GroundRegistrationForm
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ground_reg(request, id):
    reg_ground = GroundRegistration.objects.all()
    reg_match = Host_Match.objects.all()
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
        
        # Check for existing ground
        if GroundRegistration.objects.filter(uid=user).exists():
            messages.error(request, 'Ground already exist!!')
            return render(request, 'ground_reg.html', {'id': userid, 'dis': dis})
        if GroundRegistration.objects.filter(ground_name=groundname).exists():
            messages.error(request, 'Ground name already exist!!')
            return render(request, 'ground_reg.html', {'id': userid, 'dis': dis})
        
        ob = GroundRegistration(
            uid=userid,
            ground_name=groundname,
            ground_location=location,
            ground_address=address,
            ground_desc=description,
            ground_feature=features,
            ground_rate=rate,
            ground_img=img,
            is_available=1
        )
        ob.save()
        messages.success(request, 'Ground registered successfully!')
        return redirect('index')
    else:
        return render(request, 'ground_reg.html', {'id': userid, 'dis': dis})

def match_reg(request, id):
    reg_ground = GroundRegistration.objects.filter(is_available=1)
    reg_match = Host_Match.objects.filter(is_available=1)
    dis = Registration.objects.get(id=id)
    userid = request.session['id']
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        matchname = request.POST.get('matchname')
        matchdate = request.POST.get('matchdate')
        matchdescription = request.POST.get('matchdescription')
        matchrate = request.POST.get('matchrate')
        
        # Check if the match date is in the future
        if matchdate < today:
            messages.error(request, 'Select an Upcoming Date')
            return render(request, 'match_reg.html', {'id': userid, 'dis': dis, 'reg_ground': reg_ground, 'reg_match': reg_match})
        
        # Check if the match name already exists
        if Host_Match.objects.filter(match_name=matchname).exists():
            messages.error(request, 'Match name already exists! Please choose a different name.')
            return render(request, 'match_reg.html', {'id': userid, 'dis': dis, 'reg_ground': reg_ground, 'reg_match': reg_match})
        
        # Create new match
        ob = Host_Match(
            uid=userid,
            match_name=matchname,
            match_date=matchdate,
            match_desc=matchdescription,
            match_rate=matchrate,
            is_available=1
        )
        ob.save()
        
        messages.success(request, 'Match registered successfully!')
        return redirect('index')
    
    return render(request, 'match_reg.html', {'id': userid, 'dis': dis, 'reg_ground': reg_ground, 'reg_match': reg_match})

def index(request):
    reg_ground = GroundRegistration.objects.filter(is_available=1)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    reg_match = Host_Match.objects.filter(is_available=1)

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
            'reg_match': reg_match,
            'football_grounds': football_grounds,
            'volleyball_grounds': volleyball_grounds,
            'cricket_grounds': cricket_grounds,
            'badminton_grounds': badminton_grounds,
            'tennis_grounds': tennis_grounds,
        })
    else:
        return render(request, 'index.html', {
            'reg_ground': reg_ground,
            'reg_match': reg_match,
            'football_grounds': football_grounds,
            'volleyball_grounds': volleyball_grounds,
            'cricket_grounds': cricket_grounds,
            'badminton_grounds': badminton_grounds,
            'tennis_grounds': tennis_grounds,
        })

def ground_registration(request):
    if request.method == 'POST':
        form = GroundRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            ground_name = form.cleaned_data.get('ground_name')
            location = form.cleaned_data.get('ground_location')

            # Check if the ground already exists
            if GroundRegistration.objects.filter(ground_name=ground_name, ground_location=location).exists():
                return HttpResponse('Ground already exist!!')
            else:
                form.save()
                return HttpResponse('Ground registered successfully!')
    else:
        form = GroundRegistrationForm()
    return render(request, 'ground_registration.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')

def host_match_view(request):
    return HttpResponse("Host Match View")

# PhonePe Payment View
@csrf_exempt
def phonepe_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        phonepe_url = "https://api.phonepe.com/apis/hermes/v1/checkout/initiate"
        transaction_id = "txn_12345"  # Generate a unique transaction ID
        order_id = "order_12345"  # Generate a unique order ID

        payload = {
            "merchantId": settings.PHONEPE_MERCHANT_ID,
            "transactionId": transaction_id,
            "amount": int(amount) * 100,  # Amount in paise
            "merchantOrderId": order_id,
            "redirectUrl": "https://your-redirect-url.com",
            "callbackUrl": "https://your-callback-url.com",
            "paymentModes": ["UPI"]
        }

        # Convert payload to JSON string
        payload_str = json.dumps(payload)

        # Calculate X-VERIFY header
        x_verify = hashlib.sha256((payload_str + "/apis/hermes/v1/checkout/initiate" + settings.PHONEPE_MERCHANT_KEY).encode()).hexdigest() + "###1"

        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": x_verify,
            "X-MERCHANT-ID": settings.PHONEPE_MERCHANT_ID
        }

        response = requests.post(phonepe_url, headers=headers, data=payload_str)
        return JsonResponse(response.json())
    
    return render(request, 'phonepe_payment.html')

# Google Pay Payment View
def googlepay_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        googlepay_url = "https://payments.googleapis.com/v1/payments"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.GOOGLE_PAY_MERCHANT_KEY}"
        }
        payload = {
            "merchantId": settings.GOOGLE_PAY_MERCHANT_ID,
            "transactionId": "txn_12345",  # Generate a unique transaction ID
            "amount": amount,
            "currency": "INR",
            "redirectUrl": "https://your-redirect-url.com",
            "callbackUrl": "https://your-callback-url.com"
        }
        response = requests.post(googlepay_url, headers=headers, data=json.dumps(payload))
        return JsonResponse(response.json())
    return render(request, 'googlepay_payment.html')

# Paytm Payment View
def paytm_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        paytm_url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction"
        headers = {
            "Content-Type": "application/json",
            "mid": settings.PAYTM_MERCHANT_ID,
            "key": settings.PAYTM_MERCHANT_KEY
        }
        payload = {
            "requestType": "Payment",
            "mid": settings.PAYTM_MERCHANT_ID,
            "orderId": "order_12345",  # Generate a unique order ID
            "amount": amount,
            "currency": "INR",
            "callbackUrl": "https://your-callback-url.com"
        }
        response = requests.post(paytm_url, headers=headers, data=json.dumps(payload))
        return JsonResponse(response.json())
    return render(request, 'paytm_payment.html')