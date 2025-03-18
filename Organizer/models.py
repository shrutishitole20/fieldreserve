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

class Host_Tournament(models.Model):
    uid = models.CharField(max_length=100, default='')
    tournament_name = models.CharField(max_length=100)
    tournament_date = models.CharField(max_length=20, default='')
    tournament_desc = models.CharField(max_length=750, default='')
    tournament_rate = models.CharField(max_length=50, default='')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.tournament_name