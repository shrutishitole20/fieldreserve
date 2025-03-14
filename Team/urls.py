from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *

urlpatterns = [
    path('tournament_booking/<id>',tournament_booking,name='tournament_booking'),
    path('ground_booking_details/<id>',ground_booking_details,name='ground_booking_details'),
    path('ground_booking/<id>',ground_booking,name='ground_booking'),
    path('rate/<id>',rate,name='rate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)