from django.urls import path
from .views import ground_registration, ground_reg, match_reg, index, success_view, host_match_view, phonepe_payment, googlepay_payment, paytm_payment, map_view

urlpatterns = [
    path('ground/register/', ground_registration, name='ground_registration'), 
    path('ground_reg/<int:id>/', ground_reg, name='ground_reg'), 
    path('match_reg/<int:id>/', match_reg, name='match_reg'),
    path('host_match/', host_match_view, name='host_match'),
    path('', index, name='index'),
    path('success/', success_view, name='success'),
    path('phonepe-payment/', phonepe_payment, name='phonepe_payment'),
    path('googlepay-payment/', googlepay_payment, name='googlepay_payment'),
    path('paytm-payment/', paytm_payment, name='paytm_payment'),
    path('map/', map_view, name='map_view'),
]