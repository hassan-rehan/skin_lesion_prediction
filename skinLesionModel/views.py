# from django.shortcuts import render, redirect
# from .models import Predictions
# from django.http import HttpResponse,JsonResponse
# from .model import *
# import os
# def get_prediction(request,id):
#     if 'user_id' in request.session and 'user_type' in request.session:
#         if id==request.session['user_id'] and request.session['user_type']==0:
#             if request.is_ajax():
#                 try:
#                     file=request.FILES['lesion-image']
#                     model,input_size,device=choose_model('densenet')
#                     ans=predict(file,model,input_size,device)
#                     ans_dict={  0  :  'Actinic keratoses',
#                                 1  :  'Basal cell carcinoma',
#                                 2  :  'Benign keratosis-like lesions ',
#                                 3  :  'Dermatofibroma',
#                                 4  :  'Melanocytic nevi',
#                                 5  :  'Vascular lesions',
#                                 6  :  'dermatofibroma'
#                         }
#                     return HttpResponse(ans_dict[ans])
#                 except:
#                     return HttpResponse('false')
#             else:
#                 return HttpResponse('false')
#         else:
#             return redirect('/patient/'+str(request.session['user_id'])+'/profile')
#     else:
#         return redirect("/")