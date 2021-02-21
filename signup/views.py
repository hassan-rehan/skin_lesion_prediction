from django.shortcuts import render, redirect
from .models import Users, Certificates
import datetime
# Create your views here.

def patient_signup(request):
    if request.method == 'GET':
        return render(request,'patient-signup.html')
    elif request.method == 'POST':
        try:
            if Users.objects.filter(email=request.POST.get('email')).exists():
                return render(request,'patient-signup.html',{'info':"Account with this email already exists."})
            else:
                date=datetime.datetime.strptime(request.POST.get('dob'), "%m/%d/%Y").date()
                newUser = Users(email=request.POST.get('email'),password=request.POST.get('password'),user_type=0,date_registered=datetime.datetime.now().date(),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'),active=True,city=request.POST.get('city_name'),country=request.POST.get('country_name'),gender=request.POST.get('gender'),DOB=date)
                newUser.save()
                return render(request,'signin.html', {'info':"Registration completed successfully. Please login to use our services."})
        except:
            return render(request,'patient-signup.html',{'info':"Something went wrong. Please try again"})

def doctor_signup(request):
    if request.method == 'GET':
        return render(request,'doctor-signup.html')
    elif request.method == 'POST':
        if Users.objects.filter(email=request.POST.get('email')).exists():
            return render(request,'doctor-signup.html',{'info':"Account with this email already exists."})
        else:
            date=datetime.datetime.strptime(request.POST.get('dob'), "%m/%d/%Y").date()
            newUser = Users(email=request.POST.get('email'),password=request.POST.get('password'),user_type=1,date_registered=datetime.datetime.now().date(),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'),active=True,city=request.POST.get('city_name'),country=request.POST.get('country_name'),gender=request.POST.get('gender'),DOB=date)
            newUser.save()
            certificates = Certificates(doctor_id=newUser,specialization_area=request.POST.get('specialization'),certificate=request.FILES['degree'])
            certificates.save()
            return render(request,'signin.html', {'info':"Registration completed successfully. Please login to use our services."})
        