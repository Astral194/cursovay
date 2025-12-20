from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

from .constants import (ROLE_CHOICES, REGEX_PATTERN,
                        REGEX_PHONE_PATTERN, STATUS_CHOICES)

class SystemUser(models.Model):
    email = models.EmailField(
        unique=True,
        validators=[
            RegexValidator(
                regex=REGEX_PATTERN
            )
        ]
    )
    hashed_password = models.TextField()
    full_name = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'system_users'
        verbose_name = 'Пользователь системы'
        verbose_name_plural = 'Пользователи системы'
        ordering = ['role', ]


    def __str__(self):
        return f"{self.full_name or self.email}"



class Patient(models.Model):
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.TextField(unique=True, blank=True, null=True,
                             validators=[
                                 RegexValidator(
                                     regex=REGEX_PHONE_PATTERN
                                 )
                             ]
                             )
    email = models.EmailField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'patients'
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['created_at', ]

    def __str__(self):
        return f"{self.id}"



class EncryptionKey(models.Model):
    key_value = models.BinaryField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'encryption_keys'

    def __str__(self):
        return f"{self.id}"




class Alias(models.Model):
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='alias'
    )
    encrypted_data = models.TextField()
    key = models.ForeignKey(
        EncryptionKey,
        on_delete=models.PROTECT
    )
    iv = models.BinaryField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'aliases'
        verbose_name = 'Псевдоним пациента'
        ordering = ['patient_id']

    def __str__(self):
        return f"{self.id}"


class Doctor(models.Model):
    user = models.OneToOneField(
        SystemUser,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id'
    )
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    specialization = models.TextField(blank=True, null=True)
    license_number = models.TextField(unique=True)
    phone = models.TextField(unique=True, blank=True, null=True,
                             validators=[
                                 RegexValidator(
                                     regex=REGEX_PHONE_PATTERN
                                 )
                             ]
                             )
    email = models.EmailField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'doctors'
        verbose_name = 'Врач'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Visit(models.Model):
    alias = models.ForeignKey(
        Alias,
        on_delete=models.SET_NULL,
        null=True
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True
    )
    visit_date = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'visits'
        ordering = ['-visit_date']

    def __str__(self):
        return f"{self.id}"



class LabTest(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE
    )
    test_type = models.TextField()
    ordered_at = models.DateTimeField(default=timezone.now)
    result = models.TextField(blank=True, null=True)
    result_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'lab_tests'


class MedicalRecord(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE
    )
    record_type = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'medical_records'



class Diagnosis(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE
    )
    icd_code = models.TextField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'diagnoses'



class Medication(models.Model):
    name = models.TextField(unique=True)
    dosage = models.TextField(blank=True, null=True)
    instruction = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'medications'



class Prescription(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE
    )
    adjustments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    medications = models.ManyToManyField(
        Medication,
        through='PrescriptionMedication'
    )

    class Meta:
        db_table = 'prescriptions'



class PrescriptionMedication(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'prescription_medications'
        unique_together = ('prescription', 'medication')



class ActionLog(models.Model):
    user = models.ForeignKey(
        SystemUser,
        on_delete=models.SET_NULL,
        null=True
    )
    action_type = models.TextField()
    entity = models.TextField()
    entity_id = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'action_logs'
