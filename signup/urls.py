from django.urls import path
from . import views

urlpatterns= [
    path('patient/',views.patient_signup,name='patient_signup'),
    path('doctor/',views.doctor_signup,name='doctor_signup')
]