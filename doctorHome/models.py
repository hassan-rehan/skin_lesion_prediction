from django.db import models
from signup.models import Users
import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'profilePictures/doctors'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(str(instance.pk)+"_d", ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class DoctorProfiles(models.Model):
    introduction=models.TextField()
    office_address= models.TextField()
    doctor_id = models.ForeignKey(Users,db_column="doctor_id",primary_key=True,on_delete=models.CASCADE)
    pic = models.ImageField(upload_to=path_and_rename,null=True,blank=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
