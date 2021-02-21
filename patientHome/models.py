from django.db import models
from signup.models import Users
import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'profilePictures/patients'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(str(instance.pk)+"_p", ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class PatientProfiles(models.Model):
    patient_id = models.ForeignKey(Users,db_column="patient_id",primary_key=True,on_delete=models.CASCADE)
    introduction = models.TextField()
    pic = models.ImageField(upload_to=path_and_rename,null=True,blank=True)
    occupation = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20,null=True,blank=True)
    heart_beat = models.IntegerField(null=True,blank=True)
    blood_pressure = models.IntegerField(null=True,blank=True)
    sugar = models.IntegerField(null=True,blank=True)
    haemoglobin = models.IntegerField(null=True,blank=True)

class ProposalTable(models.Model):
    proposal_data = models.TextField()
    created_at = models.DateTimeField()
    accepted = models.BooleanField()
    reported = models.BooleanField()
    patient_id = models.ForeignKey(Users,db_column="patient_id",related_name='patient_id',on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Users,db_column="doctor_id",related_name='doctor_id',on_delete=models.CASCADE)

class medical_history(models.Model):
    start_date = models.DateField()
    disease = models.TextField()
    medicines = models.TextField()
    taking_medicine = models.BooleanField()
    patient_id = models.ForeignKey(Users,db_column="patient_id",on_delete=models.CASCADE)