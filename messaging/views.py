from django.shortcuts import render
from fcm_django.models import FCMDevice
from django.http import HttpResponse

def update_fcm_token(request):
    if request.is_ajax:
        try:
            user_fcm_data = FCMDevice.objects.get(user_id=request.session['user_id'])
            user_fcm_data.registration_id=request.POST.get("fcm_token")
            user_fcm_data.save()
            return HttpResponse("True")
        except:
            return HttpResponse("False")

def FM_js(request):
    return render(request, 'firebase-messaging-sw.js', content_type="application/x-javascript")

def sendSingleMessage(request):
    device = FCMDevice.objects.get(device_id=3)
    device.send_message(title="Hassan Rehan", body="Hi there", data={"test": "test"})