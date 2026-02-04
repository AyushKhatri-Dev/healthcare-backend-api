from django.contrib import admin
from .models import Patient
# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'contact', 'address', 'medical_history', 'created_by', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['name', 'contact']
