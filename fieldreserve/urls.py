from django.contrib import admin
from django.urls import path, include
from fieldreserve import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Team.urls')),
    path('', include('Admin.urls')),
    path('', include('Organizer.urls')),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'), 
]