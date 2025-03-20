from django.db import models

# Create your models here.

class GroundRegistration(models.Model):
    uid = models.CharField(max_length=100, default='')
    ground_name = models.CharField(max_length=100)
    ground_location = models.CharField(max_length=50, default='')
    ground_address = models.CharField(max_length=50, default='')
    ground_desc = models.CharField(max_length=1000, default='')
    ground_feature = models.CharField(max_length=50, default='')
    ground_rate = models.CharField(max_length=50, default='')
    ground_img = models.ImageField(upload_to='images', default='')
    ground_type = models.CharField(max_length=50, default='')  # Add this field
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.ground_name

class Host_Match(models.Model):
    uid = models.CharField(max_length=100, default='')
    match_name = models.CharField(max_length=100)
    match_date = models.CharField(max_length=20, default='')
    match_desc = models.CharField(max_length=750, default='')
    match_rate = models.CharField(max_length=50, default='')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.match_name
class Reservation(models.Model):
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField()
    time_slot = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name} - {self.date} - {self.time_slot}"
