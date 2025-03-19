from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/<id>', about, name='about'),
    path('reg/', reg, name='reg'),
    path('login/', login, name='login'),
    path('lgout/', lgout, name='lgout'),
    path('match_about/<id>', match_about, name='match_about'),
    path('profile/', profile, name='profile'),
    path('search/', search, name='search'),
    path('cancel/<id>', cancel, name='cancel'),
    path('', include('Organizer.urls')),
    path('ground_reg/', include('Organizer.urls'), name='ground_reg'),  
]