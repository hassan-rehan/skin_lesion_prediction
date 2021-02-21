from django.shortcuts import render, redirect
from signup.models import Users
from fcm_django.models import FCMDevice

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html')
    elif request.method == 'POST':
        if Users.objects.filter(email=request.POST.get('email'),password=request.POST.get('password')).exists():
            user = Users.objects.get(email=request.POST.get('email'))
            if user.active == True :
                
                #Updating FCM token
                if FCMDevice.objects.filter(device_id=user.id).exists():
                    user_fcm_data=FCMDevice.objects.get(device_id=user.id)
                    user_fcm_data.registration_id=request.POST.get('fcm_token')
                    user_fcm_data.save()
                else:
                    new_entry = FCMDevice(registration_id=request.POST.get('fcm_token'),active=True,type='web',device_id=user.id)
                    new_entry.save()
            
                if user.user_type == 0: # 0 represent patient
                    request.session['user_id']=user.id
                    request.session['user_type']=user.user_type
                    return redirect('/patient/'+str(user.id)+'/home')
                elif user.user_type == 1: # 1 represent doctor
                    request.session['user_id']=user.id
                    request.session['user_type']=user.user_type
                    return redirect('/doctor/'+str(user.id)+'/home')
            else:
                return render(request,'signin.html',{'info':"Your account has been deleted or blocked."})
        else:
            return render(request,'signin.html',{'info':"Email or Password incorrect. Try again."})  
        