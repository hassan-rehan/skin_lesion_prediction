from django.urls import path
from . import views

urlpatterns= [
    path('home',views.patientHome),
    path('messages',views.messages),
    path('logout',views.patient_logout),
    path('profile',views.patient_profile),
    path('profile/update',views.update_patient_profile),
    path('profile/add-medical-history',views.add_medical_history),
    path('profile/delete-medical-history/<int:hid>',views.delete_medical_history),
    path('model',views.model_page),
    path('doctors_available',views.doctors_available),
    path('submit_proposal/<int:did>',views.submit_proposal),
    path('updateProfilePicture',views.updateProfilePicture),
    path('view_profile',views.view_profile),
    path('proposal/<int:pid>/delete',views.deleteProposal),
    path('proposals',views.proposals_sent),
    path('sendMessage',views.sendMessage),
]