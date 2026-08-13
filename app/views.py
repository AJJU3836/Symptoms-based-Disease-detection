from datetime import datetime

from django.db import IntegrityError
from django.shortcuts import render, redirect
from app import admin
from app.models import *


def home(request):
    try:
        return render(request, 'app/home.html')
    except Exception as ex:
        return render(request, 'app/home.html', {'message': ex})


def registration(request):
    if request.method == 'POST':
        try:
            patient = Patient()
            patient.id = datetime.now().strftime('%d%m%y%I%M%S')
            patient.mobile = str(request.POST.get('mobile')).strip()
            patient.name = request.POST.get('name')
            patient.dob = datetime.strptime(request.POST.get('dob'), '%Y-%m-%d').strftime('%d %b %Y')
            patient.gender = request.POST.get('gender')
            patient.email = request.POST.get('email')
            patient.address = request.POST.get('address')
            patient.password = str(request.POST.get('password')).strip()
            patient.save(force_insert=True)
            message = 'Patient registration done'
        except Exception as ex:
            message = ex
        return render(request, 'app/registration.html', {'message': message})
    else:
        return render(request, 'app/registration.html')


def login(request):
    try:
        if request.method == 'POST':
            mobile = str(request.POST.get("mobile")).strip()
            password = str(request.POST.get("password")).strip()
            role = str(request.POST.get("role")).strip()
            if role == 'admin':
                if mobile == admin.mobile and password == admin.password:
                    request.session['alogin'] = True
                    return redirect(patient_master)
            else:
                patient = Patient.objects.get(mobile=mobile)
                if patient.password == password:
                    request.session['plogin'] = True
                    request.session['patient'] = patient
                    return redirect(search_doctor)
            message = 'Invalid username or password'
            return render(request, 'app/login.html', {'message': message})
        else:
            request.session['alogin'] = False
            request.session['plogin'] = False
            return render(request, 'app/login.html')
    except Patient.DoesNotExist:
        message = 'Invalid username or password'
    except Exception as ex:
        message = ex
    return render(request, 'app/login.html', {'message': message})


def patient_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        patients = None
        message = ''
        try:
            if request.method == "POST":
                patient = Patient.objects.get(id=request.POST.get("id"))
                patient.delete()
                message = 'Patient details deleted successfully..'
            patients = Patient.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/patient_master.html', {'message': message, 'patients': patients})
    else:
        return redirect(login)


def add_speciality(request):
    if 'alogin' in request.session and request.session['alogin']:
        message = ''
        try:
            if request.method == "POST":
                speciality = Speciality()
                speciality.name = str(request.POST.get('name')).strip()
                speciality.save(force_insert=True)
                message = 'Speciality added successfully...'
        except Exception as ex:
            message = ex
        return render(request, 'admin/add_speciality.html', {'message': message})
    else:
        return redirect(login)


def speciality_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        specialities = None
        message = ''
        try:
            if request.method == "POST":
                speciality = Speciality.objects.get(name=request.POST.get("name"))
                speciality.delete()
                message = 'Speciality details deleted successfully..'
            specialities = Speciality.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/speciality_master.html', {'message': message, 'specialities': specialities})
    else:
        return redirect(login)


def add_symptom(request):
    if 'alogin' in request.session and request.session['alogin']:
        message = ''
        try:
            if request.method == "POST":
                specialities = request.POST.getlist('specialities')
                for speciality in specialities:
                    symptom = Symptom()
                    symptom.name = str(request.POST.get('name')).strip()
                    symptom.speciality = Speciality.objects.get(name=speciality)
                    symptom.save(force_insert=True)
                message = 'Symptom added successfully...'
            specialities = Speciality.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/add_symptom.html', {'message': message, 'specialities': specialities})
    else:
        return redirect(login)


def symptom_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        symptoms = None
        message = ''
        try:
            if request.method == "POST":
                symptom = Symptom.objects.get(name=request.POST.get("name"), speciality=request.POST.get("speciality"))
                symptom.delete()
                message = 'Symptom details deleted successfully..'
            symptoms = Symptom.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/symptom_master.html', {'message': message, 'symptoms': symptoms})
    else:
        return redirect(login)


def add_doctor(request):
    if 'alogin' in request.session and request.session['alogin']:
        message = ''
        specialities = None
        try:
            specialities = Speciality.objects.all()
            if request.method == "POST":
                if request.method == 'POST':
                    if request.FILES:
                        id_ = datetime.now().strftime('%d%m%y%I%M%S')
                        photo = request.FILES['photo']
                        with open(f'media/doctor/{id_}.jpg', 'wb') as fw:
                            fw.write(photo.read())
                        doctor = Doctor()
                        doctor.id = id_
                        doctor.name = request.POST.get('name')
                        doctor.qualification = request.POST.get('qualification')
                        doctor.mobile = str(request.POST.get('mobile')).strip()
                        doctor.email = str(request.POST.get('email')).strip()
                        doctor.address = request.POST.get('address')
                        doctor.gender = request.POST.get('gender')
                        doctor.agegroup = request.POST.get('agegroup')
                        doctor.speciality = Speciality.objects.get(name=request.POST.get('speciality'))
                        doctor.experience = request.POST.get('experience')
                        doctor.save(force_insert=True)
                        message = 'Doctor profile added successfully...'
                    else:
                        raise Exception('Photo uploading error')
        except Exception as ex:
            message = ex
        return render(request, 'admin/add_doctor.html', {'message': message, 'specialities': specialities})
    else:
        return redirect(login)


def doctor_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        doctors = None
        message = ''
        try:
            if request.method == "POST":
                doctor = Doctor.objects.get(id=request.POST.get("id"))
                doctor.delete()
                message = 'Doctor details deleted successfully..'
            doctors = Doctor.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/doctor_master.html', {'message': message, 'doctors': doctors})
    else:
        return redirect(login)


def search_doctor(request):
    if 'plogin' in request.session and request.session['plogin']:
        message = ''
        agegroup = "Adult"
        symptoms = None
        try:
            patient = request.session["patient"]
            dob = datetime.strptime(patient.dob, '%d %b %Y')
            today = datetime.today()
            age = today.year - dob.year
            if 0 <= age <= 10:
                agegroup = "Children"
            symptoms = Symptom.objects.all()
            symptoms = set(list(symptoms.values_list('name', flat=True)))
        except Exception as ex:
            message = ex
        return render(request, 'patient/search_doctor.html',
                      {'message': message, 'agegroup': agegroup, 'symptoms': symptoms})
    else:
        return redirect(login)


def recommended_doctors(request):
    if 'plogin' in request.session and request.session['plogin']:
        message = ""
        doctors = None
        try:
            if request.method == "POST":
                agegroup = str(request.POST.get('agegroup')).lower()
                symptoms = request.POST.getlist('symptoms')
                symptoms = Symptom.objects.filter(name__in=symptoms)
                specialities = set(list(symptoms.values_list('speciality', flat=True)))
                doctors = Doctor.objects.filter(speciality__in=specialities).filter(agegroup=agegroup)
            else:
                return redirect(login)
        except Exception as ex:
            message = ex
        return render(request, 'patient/recommended_doctors.html', {'message': message, 'doctors': doctors})
    else:
        return redirect(login)


def saved_doctors(request):
    if 'plogin' in request.session and request.session['plogin']:
        message = ""
        doctors = None
        patient = request.session['patient']
        try:
            if request.method == "POST":
                doctor = Doctor.objects.get(id=request.POST.get("id"))
                if "delete" in request.POST:
                    pd = PatientDoctor.objects.get(patient=patient, doctor=doctor)
                    pd.delete()
                    message = 'Doctor details removed from quick access..'
                else:
                    pd = PatientDoctor()
                    pd.patient = patient
                    pd.doctor = doctor
                    pd.save(force_insert=True)
            doctors = PatientDoctor.objects.filter(patient=patient)
        except IntegrityError:
            doctors = PatientDoctor.objects.filter(patient=patient)
        except Exception as ex:
            message = ex
        return render(request, 'patient/saved_doctors.html', {'message': message, 'doctors': doctors})
    else:
        return redirect(login)


def change_password(request):
    if 'plogin' in request.session and request.session['plogin']:
        try:
            message = ''
            if request.method == 'POST':
                patient = request.session['patient']
                oldpassword = str(request.POST.get('oldpassword')).strip()
                newpassword = str(request.POST.get('newpassword')).strip()
                if patient.password == oldpassword:
                    patient.password = newpassword
                    patient.save(force_update=True)
                    message = 'Password changed successfully'
                else:
                    raise Exception('Password not match')
        except Exception as ex:
            message = ex
        return render(request, 'patient/change_password.html', {'message': message})
    else:
        return redirect(login)
