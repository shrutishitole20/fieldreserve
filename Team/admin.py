from django.contrib import admin
from  .models import Match_Booking,Ground_Booking,rating
# Register your models here.


admin.site.register(Match_Booking)
admin.site.register(Ground_Booking)
admin.site.register(rating)