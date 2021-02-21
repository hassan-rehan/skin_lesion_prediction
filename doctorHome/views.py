from django.shortcuts import render,redirect
from .models import DoctorProfiles
from patientHome.models import ProposalTable, PatientProfiles
from signup.models import Users
from django.http import Http404
from django.http import HttpResponse
from messaging.models import ChatRooms
from messaging.models import Messages
import datetime

def doctorHome(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            return render(request,'doctorHome.html')
        else:
            return redirect("/")
    else:
        return redirect("/")


def messages(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.method == 'GET':
                messaging=[]
                if ChatRooms.objects.filter(doctor_id=id).exists():
                    chatrooms = list(ChatRooms.objects.filter(doctor_id=id))
                    for chatroom in chatrooms:
                        patient_pic = ""
                        patient = Users.objects.get(id=chatroom.patient_id.id)
                        p_name = patient.first_name+" "+patient.last_name
                        if PatientProfiles.objects.filter(patient_id=chatroom.patient_id).exists():
                            patient_pic = PatientProfiles.objects.get(patient_id=chatroom.patient_id).pic
                            if profile_pic.name == "":
                                patient_pic = ""

                        messages = list(Messages.objects.filter(room_id=chatroom.id).order_by('created_at'))
                        messaging.append({
                                        'room_id': chatroom.id,
                                        'patient_pic': patient_pic,
                                        'patient_name': p_name,
                                        'created_at': chatroom.created_at,
                                        'patient_id': chatroom.patient_id.id,
                                        'messages' : messages
                                    })
                return render(request,'doctor-messages.html',{ 'messaging':messaging })
        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/messages')
    else:
        return redirect("/")


def doctor_logout(request,id):
    request.session.clear()
    return redirect('/')

def doctor_profile(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.method == 'GET':

                doctor_data = Users.objects.get(id=id)
                
                if DoctorProfiles.objects.filter(doctor_id=id).exists():
                    profile_data = DoctorProfiles.objects.get(doctor_id=id)
                else:
                    profile_data = 0

                return render(request,'doctor-profile.html',{'profile_data': profile_data,'doctor_data':doctor_data})
        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")

def view_profile(request,id):
    if request.method == 'GET':
        doctor_data = Users.objects.get(id=id)
        if doctor_data.user_type == 1:
            if DoctorProfiles.objects.filter(doctor_id=id).exists():
                profile_data = DoctorProfiles.objects.get(doctor_id=id)
            else:
                profile_data = 0
        else:
            raise Http404("Page not found.")

        return render(request,'view_doc_profile.html',{'profile_data': profile_data,'doctor_data':doctor_data})
       

def update_profile(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.method == 'POST':
                if DoctorProfiles.objects.filter(doctor_id=id).exists():
                    doctor_profile=DoctorProfiles.objects.get(doctor_id=id)
                    doctor_profile.introduction=request.POST.get('introduction')
                    doctor_profile.office_address=request.POST.get('address')
                    doctor_profile.phone=request.POST.get('phone')
                    doctor_profile.save()
                else:
                    doctor_data = Users.objects.get(id=id)
                    doctor_profile=DoctorProfiles(
                    doctor_id=doctor_data,
                    introduction=request.POST.get('introduction'),
                    phone=request.POST.get('phone'),
                    office_address=request.POST.get('address'),
                    )
                    doctor_profile.save()

                return redirect('/doctor/'+str(request.session['user_id'])+'/profile')
        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")

def proposals_received(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.method == 'GET':
                proposals_data=[]
                if ProposalTable.objects.filter(doctor_id=id).exists():
                    data = list(ProposalTable.objects.filter(doctor_id=id))
                    for proposal in data:
                        user = Users.objects.get(id=proposal.patient_id.id)
                        name = user.first_name+" "+user.last_name
                        pic = ""          
                        if PatientProfiles.objects.filter(patient_id=proposal.patient_id.id).exists():
                            pic = PatientProfiles.objects.get(patient_id=proposal.patient_id.id).pic  
                            if pic.name == '':
                                pic = ""
                        
                        proposals_data.append({
                            'patient_id': proposal.patient_id.id,
                            'proposal_data': proposal.proposal_data,
                            'patient_pic': pic,
                            'patient_name': name,
                            'accepted': proposal.accepted,
                            'reported' : proposal.reported,
                            'created_at' : proposal.created_at,
                            'key' : proposal.id
                        })  

                return render(request,'doc_proposals.html',{'proposals_data': proposals_data})
        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/proposals')
    else:
        return redirect("/")

def updateProfilePicture(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.is_ajax():
                user_profile = DoctorProfiles.objects.get(doctor_id=id)
                user_profile.pic = request.FILES['new-profile-pic']
                user_profile.save()
                return HttpResponse(user_profile.pic.url)
            else:
                return HttpResponse("false")

        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")

def deleteProposal(request,id,pid):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.is_ajax():
                if ProposalTable.objects.filter(id=pid).exists():
                    proposal = ProposalTable.objects.get(id=pid)
                    if proposal.doctor_id.id == id:
                        proposal.delete()
                        return HttpResponse("true")
                    else:
                        return HttpResponse("false")
                else:
                    return HttpResponse("false")
            else:
                return HttpResponse("false")

        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/proposals')
    else:
        return redirect("/")

def reportProposal(request,id,pid):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.is_ajax():
                if ProposalTable.objects.filter(id=pid).exists():
                    proposal = ProposalTable.objects.get(id=pid)
                    if proposal.doctor_id.id == id:
                        proposal.reported = True
                        proposal.save()
                        return HttpResponse("true")
                    else:
                        return HttpResponse("false")
                else:
                    return HttpResponse("false")
            else:
                return HttpResponse("false")

        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/proposals')
    else:
        return redirect("/")

def acceptProposal(request,id,pid):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.is_ajax():
                if ProposalTable.objects.filter(id=pid).exists():
                    proposal = ProposalTable.objects.get(id=pid)
                    if proposal.doctor_id.id == id:
                        proposal.accepted = True
                        proposal.save()
                        if not ChatRooms.objects.filter(patient_id=proposal.patient_id).filter(doctor_id=proposal.doctor_id).exists():
                            chatroom = ChatRooms(
                            created_at=datetime.datetime.now(),
                            patient_id=proposal.patient_id,
                            doctor_id=proposal.doctor_id
                            )
                            chatroom.save()
                            message=Messages(
                            sender_id=proposal.doctor_id,
                            room_id=chatroom,
                            message="Proposal is accepted. We can now chat about problem mentioned in proposal.",
                            created_at=datetime.datetime.now()
                            )
                            message.save()
                        else:
                            existing_room = list(ChatRooms.objects.filter(patient_id=proposal.patient_id).filter(doctor_id=proposal.doctor_id))
                            message=Messages(
                            sender_id=proposal.doctor_id,
                            room_id=existing_room[0],
                            message="Proposal is accepted. We can now chat about problem mentioned in proposal.",
                            created_at=datetime.datetime.now()
                            )
                            message.save()
                        return HttpResponse("true")
                    else:
                        return HttpResponse("false")
                else:
                    return HttpResponse("false")
            else:
                return HttpResponse("false")

        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/proposals')
    else:
        return redirect("/")

def sendMessage(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==1:
            if request.is_ajax():
                room_id = request.POST.get("room_id")
                msg = request.POST.get("message")
                if ChatRooms.objects.filter(id=room_id).exists():
                    chatroom = ChatRooms.objects.get(id=room_id)
                    message = Messages(
                    sender_id = chatroom.doctor_id,
                    room_id = chatroom,
                    message = msg,
                    created_at = datetime.datetime.now()
                    )
                    message.save()
                    return HttpResponse("true")
                else:
                    return HttpResponse("false")
            else:
                return HttpResponse("false")

        else:
            return redirect('/doctor/'+str(request.session['user_id'])+'/messages')
    else:
        return redirect("/")