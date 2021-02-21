from django.db import models
from signup.models import Users

class ChatRooms(models.Model):
    created_at = models.DateTimeField()
    patient_id = models.ForeignKey(Users,db_column="patient_id",related_name='pat_id',on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Users,db_column="doctor_id",related_name='doc_id',on_delete=models.CASCADE)
    
class Messages(models.Model):
    sender_id = models.ForeignKey(Users,db_column="sender_id",on_delete=models.CASCADE)
    room_id = models.ForeignKey(ChatRooms,db_column="room_id",on_delete=models.CASCADE)
    message = models.TextField()
    seen_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField()

class NotificationTable(models.Model):
    reference_id = models.IntegerField()
    platform = models.TextField()
    read_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField()