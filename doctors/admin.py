from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'experience_years', 'available', 'created_at']
    list_filter = ['specialization', 'available']
    search_fields = ['name', 'email']