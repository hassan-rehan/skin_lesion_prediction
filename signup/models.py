from django.db import models

class Users(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=20)
    user_type = models.IntegerField()
    date_registered = models.DateField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    active = models.BooleanField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    gender = models.IntegerField()
    DOB = models.DateField()

class Certificates(models.Model):
    doctor_id = models.ForeignKey(Users,db_column="doctor_id",primary_key=True,on_delete=models.CASCADE)
    certificate = models.FileField()
    specialization_area = models.CharField(max_length=50)