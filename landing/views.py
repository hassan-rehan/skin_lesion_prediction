from django.shortcuts import render,redirect
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def landingPage(request):
    if 'user_id' in request.session and 'user_type' in request.session:
        if(request.session['user_type']==0):
            return redirect('/patient/'+str(request.session['user_id'])+'/home')
        elif(request.session['user_type']==1):
            return redirect('/doctor/'+str(request.session['user_id'])+'/home')
        else:
            return redirect('/')
    else:    
        return render(request,'landing.html')

@ensure_csrf_cookie
def careersPage(request):
    return render(request,'careers.html')