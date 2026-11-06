from datetime import datetime
import os

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.conf import settings
from app import admin
from app.models import *


# ── Helpers ───────────────────────────────────────────────────────────────────
def _ml_ready():
    """Return True if the trained model file exists."""
    model_path = os.path.join(settings.BASE_DIR, "app", "ml", "disease_model.pkl")
    return os.path.exists(model_path)


# ── Public pages ──────────────────────────────────────────────────────────────
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
            mobile   = str(request.POST.get("mobile")).strip()
            password = str(request.POST.get("password")).strip()
            role     = str(request.POST.get("role")).strip()
            if role == 'admin':
                if mobile == admin.mobile and password == admin.password:
                    request.session['alogin'] = True
                    return redirect(patient_master)
            else:
                patient = Patient.objects.get(mobile=mobile)
                if patient.password == password:
                    request.session['plogin'] = True
                    request.session['patient'] = patient
                    return redirect(check_symptoms)
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


# ── Admin views ───────────────────────────────────────────────────────────────
def patient_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        patients = None
        message  = ''
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
                speciality      = Speciality()
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
        message      = ''
        try:
            if request.method == "POST":
                speciality = Speciality.objects.get(name=request.POST.get("name"))
                speciality.delete()
                message = 'Speciality deleted successfully..'
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
                    symptom          = Symptom()
                    symptom.name     = str(request.POST.get('name')).strip()
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
        message  = ''
        try:
            if request.method == "POST":
                symptom = Symptom.objects.get(
                    name=request.POST.get("name"),
                    speciality=request.POST.get("speciality")
                )
                symptom.delete()
                message = 'Symptom deleted successfully..'
            symptoms = Symptom.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/symptom_master.html', {'message': message, 'symptoms': symptoms})
    else:
        return redirect(login)


def add_disease(request):
    if 'alogin' in request.session and request.session['alogin']:
        message      = ''
        specialities = None
        try:
            specialities = Speciality.objects.all()
            if request.method == "POST":
                disease             = Disease()
                disease.name        = str(request.POST.get('name')).strip()
                disease.description = str(request.POST.get('description')).strip()
                disease.precautions = str(request.POST.get('precautions')).strip()
                disease.speciality  = Speciality.objects.get(name=request.POST.get('speciality'))
                disease.save(force_insert=True)
                message = 'Disease added successfully...'
        except Exception as ex:
            message = ex
        return render(request, 'admin/add_disease.html', {'message': message, 'specialities': specialities})
    else:
        return redirect(login)


def disease_master(request):
    if 'alogin' in request.session and request.session['alogin']:
        diseases = None
        message  = ''
        try:
            if request.method == "POST":
                disease = Disease.objects.get(name=request.POST.get("name"))
                disease.delete()
                message = 'Disease deleted successfully..'
            diseases = Disease.objects.all()
        except Exception as ex:
            message = ex
        return render(request, 'admin/disease_master.html', {'message': message, 'diseases': diseases})
    else:
        return redirect(login)


def model_performance(request):
    """Admin page — shows ML model accuracy charts and classification report."""
    if 'alogin' in request.session and request.session['alogin']:
        context = {'ml_ready': _ml_ready()}
        if _ml_ready():
            try:
                from app.ml.predictor import get_model_info
                meta = get_model_info()
                results = meta.get("model_results", {})
                report  = meta.get("classification_report", {})

                # Build per-disease report rows
                disease_rows = []
                for disease, scores in report.items():
                    if isinstance(scores, dict) and "precision" in scores:
                        disease_rows.append({
                            "disease":   disease,
                            "precision": round(scores.get("precision", 0) * 100, 1),
                            "recall":    round(scores.get("recall", 0) * 100, 1),
                            "f1":        round(scores.get("f1-score", 0) * 100, 1),
                            "support":   int(scores.get("support", 0)),
                        })

                context.update({
                    "best_model":   meta.get("best_model"),
                    "model_results": results,
                    "disease_rows": disease_rows,
                    "total_diseases": len(meta.get("all_diseases", [])),
                    "total_symptoms": len(meta.get("all_symptoms", [])),
                })
            except Exception as ex:
                context['error'] = str(ex)
        return render(request, 'admin/model_performance.html', context)
    else:
        return redirect(login)


def retrain_model(request):
    """Admin action — retrain ML model."""
    if 'alogin' in request.session and request.session['alogin']:
        message = ''
        try:
            import subprocess, sys
            manage_py = os.path.join(settings.BASE_DIR, "app", "ml", "train_model.py")
            python    = sys.executable
            result    = subprocess.run(
                [python, manage_py],
                capture_output=True, text=True, timeout=300,
                cwd=settings.BASE_DIR
            )
            if result.returncode == 0:
                message = "✅ Model retrained successfully!"
            else:
                message = f"❌ Training failed: {result.stderr[-500:]}"
        except Exception as ex:
            message = f"❌ Error: {ex}"
        return render(request, 'admin/model_performance.html',
                      {'ml_ready': _ml_ready(), 'message': message})
    else:
        return redirect(login)


# ── Patient views ─────────────────────────────────────────────────────────────
def check_symptoms(request):
    if 'plogin' in request.session and request.session['plogin']:
        message  = ''
        symptoms = []
        try:
            # If ML model is ready, use its symptom list; else fall back to DB
            if _ml_ready():
                from app.ml.predictor import get_model_info
                meta     = get_model_info()
                symptoms = sorted([s.replace("_", " ").title() for s in meta.get("all_symptoms", [])])
            else:
                db_syms  = Symptom.objects.all()
                symptoms = sorted(set(db_syms.values_list('name', flat=True)))
                message  = "⚠ ML model not trained yet — using database symptoms."
        except Exception as ex:
            message = str(ex)
        return render(request, 'patient/check_symptoms.html',
                      {'message': message, 'symptoms': symptoms, 'ml_ready': _ml_ready()})
    else:
        return redirect(login)


def detected_diseases(request):
    if 'plogin' in request.session and request.session['plogin']:
        message     = ""
        predictions = []
        selected    = []
        severity    = ""
        try:
            if request.method == "POST":
                selected = request.POST.getlist('symptoms')
                severity = request.POST.get('severity', '')
                history  = request.POST.get('history', '')
                allergies = request.POST.get('allergies', '')
                hp        = request.POST.get('hp', '')

                if not selected:
                    message = "Please select at least one symptom."
                elif _ml_ready():
                    from app.ml.predictor import predict_diseases, get_disease_info
                    raw_preds = predict_diseases(selected, top_n=5)

                    for pred in raw_preds:
                        info = get_disease_info(pred["disease"])
                        predictions.append({
                            **pred,
                            "description": info.get("description", ""),
                            "precautions": info.get("precautions", []),
                        })
                else:
                    # Fallback — DB-based detection
                    symptoms_qs = Symptom.objects.filter(name__in=selected)
                    specialities = set(symptoms_qs.values_list('speciality', flat=True))
                    diseases_qs  = Disease.objects.filter(speciality__in=specialities)
                    for d in diseases_qs:
                        predictions.append({
                            "disease":     d.name,
                            "confidence":  None,
                            "rank":        len(predictions) + 1,
                            "description": d.description,
                            "precautions": [p.strip() for p in d.precautions.split(",") if p.strip()],
                        })
                    message = "⚠ ML model not trained — showing database-based results."
            else:
                return redirect(check_symptoms)
        except Exception as ex:
            message = str(ex)

        return render(request, 'patient/detected_diseases.html', {
            'message':     message,
            'predictions': predictions,
            'selected':    selected,
            'severity':    severity,
            'ml_ready':    _ml_ready(),
        })
    else:
        return redirect(login)


def change_password(request):
    if 'plogin' in request.session and request.session['plogin']:
        try:
            message = ''
            if request.method == 'POST':
                patient     = request.session['patient']
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
