from django.urls import path
from . import views

urlpatterns= [
  path('update_token',views.update_fcm_token,name='update_fcm_token'),
  path('send_message',views.sendSingleMessage)
]