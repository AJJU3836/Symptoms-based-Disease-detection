"""VR URL Configuration"""
from django.conf.urls.static import static
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import app.views
from VR import settings

routes = [
    ('',                    app.views.home),
    ('registration',        app.views.registration),
    ('login',               app.views.login),
    # ── Admin ────────────────────────────────────────────────────────────────
    ('patientmaster',       app.views.patient_master),
    ('addspeciality',       app.views.add_speciality),
    ('addsymptom',          app.views.add_symptom),
    ('specialitymaster',    app.views.speciality_master),
    ('symptommaster',       app.views.symptom_master),
    ('adddisease',          app.views.add_disease),
    ('diseasemaster',       app.views.disease_master),
    ('modelperformance',    app.views.model_performance),
    ('retrainmodel',        app.views.retrain_model),
    # ── Patient ──────────────────────────────────────────────────────────────
    ('checksymptoms',       app.views.check_symptoms),
    ('detected_diseases',   app.views.detected_diseases),
    ('changepassword',      app.views.change_password),
]

urlpatterns = []
for route, view in routes:
    if route == '':
        urlpatterns.append(path('', view))
    else:
        urlpatterns.append(path(route, view))
        urlpatterns.append(path(f"{route}/", view))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
