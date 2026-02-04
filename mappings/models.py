from django.db import models
from patients.models import Patient
from doctors.models import Doctor

# Create your models here.
class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name = 'doctor_mappings',
        help_text = "Patient in this mapping"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete = models.CASCADE,
        related_name = 'patient_mappings',
        help_text = "Doctor assigned to patient"
    )

    assigned_date = models.DateTimeField(auto_now_add=True, help_text = "When assignment was made")
    notes = models.TextField(blank=True, null=True, help_text = "Special notes about this assignment")
    is_active = models.BooleanField(default=True, help_text = "Is this assignment currently active")

    class Meta:
        unique_together = ('patient', 'doctor')
        ordering = ['-assigned_date']
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'

    def __str__(self):
        return f"{self.patient.name} -> Dr. {self.doctor.name}"