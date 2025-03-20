from email.policy import default
from django.db import models

# Create your models here.

class Match_Booking(models.Model):
    uid = models.CharField(max_length=100, default='')
    user_name = models.CharField(max_length=100, default='')
    mid = models.CharField(max_length=100)
    match_name= models.CharField(max_length=100, default='')
    ground_id = models.CharField(max_length=100, default='')

    def __str__(self)  -> str:
        return str(self.match_name)+" : "+str(self.user_name)

class Ground_Booking(models.Model):
    uid = models.CharField(max_length=100, default='')
    user_name = models.CharField(max_length=100, default='')
    Ground_name = models.CharField(max_length=100, default='')
    ground_id = models.CharField(max_length=100, default='')
    date = models.CharField(max_length=100, default='')
    start_time = models.CharField(max_length=100, default='')
    end_time = models.CharField(max_length=100, default='')
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.start_time) +" : "+ str(self.Ground_name)

class Rating(models.Model):
    uid = models.CharField(max_length=100, default='')
    user_name = models.CharField(max_length=100, default='')
    Ground_name = models.CharField(max_length=100, default='')
    ground_id = models.CharField(max_length=100, default='')
    star = models.IntegerField(default=0) 

    def __str__(self) -> str:
        return str(self.user_name) + " : " + str(self.Ground_name)