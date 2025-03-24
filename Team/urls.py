from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *

urlpatterns = [
    path('match_booking/<id>', match_booking, name='match_booking'),
    path('ground_booking_details/<id>', ground_booking_details, name='ground_booking_details'),
    path('ground_booking/<id>', ground_booking, name='ground_booking'),
    path('rate/<id>', rate, name='rate'),
    path('ground_booking/<int:id>/', ground_booking, name='ground_booking'),
    path('payment_page/', payment_page, name='payment_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)