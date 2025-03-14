from django.contrib import admin
from  .models import Tournament_Booking,Ground_Booking,rating
# Register your models here.


admin.site.register(Tournament_Booking)
admin.site.register(Ground_Booking)
admin.site.register(rating)