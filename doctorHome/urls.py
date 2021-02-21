from django.urls import path
from . import views

urlpatterns= [
    path('home',views.doctorHome,name='doctorHome'),
    path('messages',views.messages),
    path('logout',views.doctor_logout),
    path('profile',views.doctor_profile),
    path('view_profile',views.view_profile),
    path('profile/update',views.update_profile),
    path('proposals',views.proposals_received),
    path('sendMessage',views.sendMessage),
    path('updateProfilePicture',views.updateProfilePicture),
    path('proposal/<int:pid>/delete',views.deleteProposal),
    path('proposal/<int:pid>/report',views.reportProposal),
    path('proposal/<int:pid>/accept',views.acceptProposal),
    #path('proposal/<int:pid>/accept',views.acceptProposal),
]