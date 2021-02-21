from django.shortcuts import render, redirect
from .models import PatientProfiles
from .models import medical_history
from .models import ProposalTable
from signup.models import Users
from django.http import HttpResponse,JsonResponse
import datetime
from doctorHome.models import DoctorProfiles
from django.http import Http404
from messaging.models import ChatRooms, Messages

def patientHome(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            return render(request,'patientHome.html')
        else:
            return redirect("/")
    else:
        return redirect("/")


def messages(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.method == 'GET': 
                messaging=[]
                if ChatRooms.objects.filter(patient_id=id).exists():
                    chatrooms = list(ChatRooms.objects.filter(patient_id=id))
                    for chatroom in chatrooms:
                        doctor_pic = ""
                        doctor = Users.objects.get(id=chatroom.doctor_id.id)
                        d_name = doctor.first_name+" "+doctor.last_name
                        if DoctorProfiles.objects.filter(doctor_id=chatroom.doctor_id).exists():
                            doctor_pic = DoctorProfiles.objects.get(doctor_id=chatroom.doctor_id).pic
                            if doctor_pic.name == "":
                                doctor_pic = ""

                        messages = list(Messages.objects.filter(room_id=chatroom.id).order_by('created_at'))
                        messaging.append({
                                        'room_id': chatroom.id,
                                        'doctor_pic': doctor_pic,
                                        'doctor_name': d_name,
                                        'created_at': chatroom.created_at,
                                        'doctor_id': chatroom.doctor_id.id,
                                        'messages' : messages
                                    })
                return render(request,'patient-messages.html',{ 'messaging':messaging })
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/home')
    else:
        return redirect("/")


def patient_profile(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.method == 'GET':

                patient_data = Users.objects.get(id=id)
                
                if PatientProfiles.objects.filter(patient_id=id).exists():
                    profile_data = PatientProfiles.objects.get(patient_id=id)
                else:
                    profile_data = 0
                
                if medical_history.objects.filter(patient_id=id).exists():
                    history = list(medical_history.objects.filter(patient_id=id))
                else:
                    history = 0

                return render(request,'patient-profile.html',{'profile_data': profile_data,'history':history,'patient_data':patient_data})
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")

def update_patient_profile(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.method == 'POST':
                if PatientProfiles.objects.filter(patient_id=id).exists():
                    patient_profile=PatientProfiles.objects.get(patient_id=id)
                    patient_profile.introduction=request.POST.get('introduction')
                    patient_profile.occupation=request.POST.get('occupation')
                    patient_profile.address=request.POST.get('address')
                    patient_profile.phone=request.POST.get('phone')
                    patient_profile.heart_beat=request.POST.get('heart_beat')
                    patient_profile.blood_pressure=request.POST.get('blood_pressure')
                    patient_profile.sugar=request.POST.get('sugar')
                    patient_profile.haemoglobin=request.POST.get('haemoglobin')
                    patient_profile.save()
                else:
                    patient_data = Users.objects.get(id=id)
                    patient_profile=PatientProfiles(
                    patient_id=patient_data,
                    introduction=request.POST.get('introduction'),
                    occupation=request.POST.get('occupation'),
                    address=request.POST.get('address'),
                    phone=request.POST.get('phone'),
                    heart_beat=request.POST.get('heart_beat'),
                    blood_pressure=request.POST.get('blood_pressure'),
                    sugar=request.POST.get('sugar'),
                    haemoglobin=request.POST.get('haemoglobin')
                    )
                    patient_profile.save()

                return redirect('/patient/'+str(request.session['user_id'])+'/profile')
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")


def add_medical_history(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.is_ajax():
                user = Users.objects.get(id=request.session['user_id'])
                date = datetime.datetime.strptime(request.POST['h_date'], "%m/%d/%Y").date()
                new_history = medical_history(
                start_date = date,
                disease = request.POST['h_disease'],
                medicines = request.POST['h_medicines'],
                taking_medicine = bool(request.POST['h_medicine_status']),
                patient_id = user,
                )
                new_history.save()
                html = ( "<tr class='history-row text-center'>"
                            "<td>"
                                "<i class='fas fa-calendar-alt text-primary'></i> "+str(new_history.start_date)+
                            "</td>"
                            "<td>"           
                                +new_history.disease+
                            "</td>"
                            "<td>"
                                "<i class='fas fa-pills text-danger'></i>  "+new_history.medicines+
                            "</td>"
                            "<td>"
                                +str(new_history.taking_medicine)+
                            "</td>"
                            "<td>"
                                "<a class='remove-history-link' href='/patient/"+str(request.session['user_id'])+"/profile/delete-medical-history/"+str(new_history.id)+"' >"
                                    "<i class='fas fa-trash-alt text-warning'></i>"
                                "</a>"
                            "</td>"
                        "</tr>" )
                return HttpResponse(html)
            else:
                return HttpResponse('false')
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")


def delete_medical_history(request,id,hid):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.is_ajax():
                if medical_history.objects.filter(id=hid).exists():
                    medical_history.objects.filter(id=hid).delete()
                    return HttpResponse('true')
                else:
                    return HttpResponse('false')
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")

def model_page(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.method=='GET':
                return render(request,'model_page.html')
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")


def submit_proposal(request, id, did):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.is_ajax():
                if did == int(request.POST['doctor-id']) and Users.objects.filter(id=did).exists():
                    doctor = Users.objects.get(id=did)
                    current_user = Users.objects.get(id=id)
                    if doctor.user_type == 1:
                        date = datetime.datetime.now()
                        new_proposal = ProposalTable(
                        proposal_data=request.POST["my-proposal"],
                        created_at=date,
                        accepted=False,
                        reported=False,
                        patient_id=current_user,
                        doctor_id=doctor,
                        )
                        new_proposal.save()
                        return HttpResponse('true')
                    else:
                        return HttpResponse('false')
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/doctors_available')
    else:
        return redirect("/")

def patient_logout(request,id):
    request.session.clear()
    return redirect('/')

def doctors_available(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.method=='GET':
                doctors=[]
                doc_users = Users.objects.filter(user_type=1)
                for doc in doc_users:
                    if DoctorProfiles.objects.filter(doctor_id=doc.id).exists():
                        profile_data=DoctorProfiles.objects.get(doctor_id=doc.id)
                        pic = ""
                        if profile_data.pic.name != '':
                            pic = profile_data.pic

                        doctors.append({
                            'id': doc.id,
                            'introduction': profile_data.introduction,
                            'pic': pic,
                            'phone': profile_data.phone,
                            'office_address': profile_data.office_address,
                        })

                return render(request,'filter_doctor.html',{'doctors':doctors})
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/doctors_available')
    else:
        return redirect("/")

def updateProfilePicture(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.is_ajax():
                user_profile = PatientProfiles.objects.get(patient_id=id)
                user_profile.pic = request.FILES['new-profile-pic']
                user_profile.save()
                return HttpResponse(user_profile.pic.url)
            else:
                return HttpResponse("false")

        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/profile')
    else:
        return redirect("/")

def view_profile(request,id):
    if request.method == 'GET':
        patient_data = Users.objects.get(id=id)
        if patient_data.user_type == 0:
            if PatientProfiles.objects.filter(patient_id=id).exists():
                profile_data = PatientProfiles.objects.get(patient_id=id)
            else:
                profile_data = 0

            if medical_history.objects.filter(patient_id=id).exists():
                history = list(medical_history.objects.filter(patient_id=id))
            else:
                history = 0

        else:
            raise Http404("Page not found.")

        return render(request,'view_patient_profile.html',{'profile_data': profile_data,'patient_data':patient_data,'history':history})

def deleteProposal(request,id,pid):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.is_ajax():
                if ProposalTable.objects.filter(id=pid).exists():
                    proposal = ProposalTable.objects.get(id=pid)
                    if proposal.patient_id.id == id:
                        proposal.delete()
                        return HttpResponse("true")
                    else:
                        return HttpResponse("false")
                else:
                    return HttpResponse("false")
            else:
                return HttpResponse("false")

        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/proposals')
    else:
        return redirect("/")

def proposals_sent(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.method == 'GET':
                proposals_data=[]
                if ProposalTable.objects.filter(patient_id=id).exists():
                    data = list(ProposalTable.objects.filter(patient_id=id))
                    for proposal in data:
                        user = Users.objects.get(id=proposal.doctor_id.id)
                        name = user.first_name+" "+user.last_name
                        pic = ""          
                        if DoctorProfiles.objects.filter(doctor_id=proposal.doctor_id.id).exists():
                            pic = DoctorProfiles.objects.get(doctor_id=proposal.doctor_id.id).pic  
                            if pic.name == '':
                                pic = ""
                                
                        proposals_data.append({
                            'doctor_id': proposal.doctor_id.id,
                            'proposal_data': proposal.proposal_data,
                            'doctor_pic': pic,
                            'doctor_name': name,
                            'accepted': proposal.accepted,
                            'reported' : proposal.reported,
                            'created_at' : proposal.created_at,
                            'key' : proposal.id
                        })  

                return render(request,'patient_proposals.html',{'proposals_data': proposals_data})
        else:
            return redirect('/patient/'+str(request.session['user_id'])+'/proposals')
    else:
        return redirect("/")

def sendMessage(request,id):
    if 'user_id' in request.session and 'user_type' in request.session:
        if id==request.session['user_id'] and request.session['user_type']==0:
            if request.is_ajax():
                room_id = request.POST.get("room_id")
                msg = request.POST.get("message")
                if ChatRooms.objects.filter(id=room_id).exists():
                    chatroom = ChatRooms.objects.get(id=room_id)
                    message = Messages(
                    sender_id = chatroom.patient_id,
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
            return redirect('/patient/'+str(request.session['user_id'])+'/messages')
    else:
        return redirect("/")