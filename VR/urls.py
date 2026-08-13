"""VR URL Configuration

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
from django.conf.urls.static import static
from django.urls import path
import app.views
from VR import settings

urlpatterns = [
                  path('', app.views.home),
                  path('registration', app.views.registration),
                  path('login', app.views.login),
                  path('patientmaster', app.views.patient_master),
                  path('addspeciality', app.views.add_speciality),
                  path('addsymptom', app.views.add_symptom),
                  path('specialitymaster', app.views.speciality_master),
                  path('symptommaster', app.views.symptom_master),
                  path('adddoctor', app.views.add_doctor),
                  path('doctormaster', app.views.doctor_master),
                  path('searchdoctor', app.views.search_doctor),
                  path('recommended_doctors', app.views.recommended_doctors),
                  path('saveddoctors', app.views.saved_doctors),
                  path('changepassword', app.views.change_password),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
