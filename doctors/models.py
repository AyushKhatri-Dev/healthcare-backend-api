from django.db import models

# Create your models here.
class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('CARDIOLOGY', 'Cardiology'),
        ('NEUROLOGY', 'Neurology'),
        ('PEDIATRICS', 'Pediatrics'),
        ('ORTHOPEDICS', 'Orthopedics'),
        ('DERMATOLOGY', 'Dermatology'),
        ('GENERAL', 'General Physician'),
    ]
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices = SPECIALIZATION_CHOICES)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    experience_years = models.IntegerField(help_text="Years of experience")
    qualification = models.CharField(max_length=255, help_text="MBBS, MD, etc.")
    available = models.BooleanField(default=True, help_text="Currently available for patients")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['name']
        # verbose = 'Doctor'
        # verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

       