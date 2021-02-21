"""SkinLesionPrediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.conf import settings
from messaging import views as messaging_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',include('landing.urls')),
    path('signup/',include('signup.urls')),
    path('signin/',include('signin.urls')),
    path('patient/<int:id>/',include('patientHome.urls')),
    path('doctor/<int:id>/',include('doctorHome.urls')),
    path('patient/<int:id>/models/skin-lesion/',include('skinLesionModel.urls')),
    path('fcm/',include('messaging.urls')),
    path('firebase-messaging-sw.js',messaging_views.FM_js)
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
