from django.urls import path
from .views import *

urlpatterns = [
    path('ground_reg/<id>',ground_reg,name='ground_reg'),
    path('tournament_reg/<id>',tournament_reg,name='tournament_reg'),
    path('host_tournament/',host_tournament_view, name='host_tournament'), 
    path('success/',success_view, name='success'), 
    ]