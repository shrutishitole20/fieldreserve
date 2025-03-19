from django.urls import path
from .views import ground_reg, match_reg, index, success_view, host_match_view

urlpatterns = [
    path('ground_reg/<int:id>/', ground_reg, name='ground_reg'), 
    path('match_reg/<int:id>/', match_reg, name='match_reg'),
    path('host_match/', host_match_view, name='host_match'),
    path('', index, name='index'),
    path('success/', success_view, name='success'),
]