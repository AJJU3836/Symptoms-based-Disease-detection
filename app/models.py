from django.db import models
from viewflow.fields import CompositeKey


class Patient(models.Model):
    id = models.TextField(primary_key=True)
    mobile = models.TextField()
    name = models.TextField()
    dob = models.TextField()
    gender = models.TextField()
    address = models.TextField()
    email = models.TextField()
    password = models.TextField()

    class Meta:
        db_table = 'tblPatient'


class Speciality(models.Model):
    name = models.TextField(primary_key=True)

    class Meta:
        db_table = 'tblSpeciality'


class Symptom(models.Model):
    id = CompositeKey(columns=['name', 'speciality'])
    name = models.TextField()
    speciality = models.ForeignKey(Speciality, on_delete=models.RESTRICT)
    unique_together = (('name', 'speciality'),)

    class Meta:
        db_table = 'tblSymptom'


class Doctor(models.Model):
    id = models.TextField(primary_key=True)
    mobile = models.TextField()
    name = models.TextField()
    qualification = models.TextField()
    gender = models.TextField()
    address = models.TextField()
    email = models.TextField()
    experience = models.TextField()
    agegroup = models.TextField()
    speciality = models.ForeignKey(Speciality, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'tblDoctor'


class PatientDoctor(models.Model):
    id = CompositeKey(columns=['patient_id', 'doctor_id'])
    patient = models.ForeignKey(Patient, on_delete=models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    unique_together = (('patient', 'doctor'),)

    class Meta:
        db_table = 'tblPatientDoctor'
