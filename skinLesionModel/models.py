from django.db import models
from signup.models import Users

class Predictions(models.Model):
    patient_id = models.ForeignKey(Users,db_column="patient_id",on_delete=models.CASCADE)
    result = models.BooleanField()
    cancer_type = models.IntegerField()
    image = models.ImageField()
