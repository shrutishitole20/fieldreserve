from django.urls import path
from .views import ground_reg, tournament_reg, index, success_view, host_tournament_view

urlpatterns = [
    path('ground_reg/<int:id>/', ground_reg, name='ground_reg'), 
    path('tournament_reg/<int:id>/', tournament_reg, name='tournament_reg'),
    path('host_tournament/', host_tournament_view, name='host_tournament'),
    path('', index, name='index'),
    path('success/', success_view, name='success'),
]