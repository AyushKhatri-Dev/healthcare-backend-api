from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model
    
    Handles all CRUD operations for doctors
    """

    # Display specialization name
    specialization_display = serializers.CharField(
        source='get_specialization_display', 
        read_only=True
    )

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'specialization',
            'specialization_display', 
            'contact',
            'email',
            'experience_years',
            'qualification',
            'available',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_experience_years(self, value):
        """
        Validate experience years
        """
        if value < 0:
            raise serializers.ValidationError("Experience cannot be negative")
        if value > 70:
            raise serializers.ValidationError("Experience seems unrealistic (max 70 years)")
        return value
    
    def validate_contact(self, value):
        """
        Validate contact number
        """
        if not value.isdigit():
            raise serializers.ValidationError("Contact must contain only digits")
        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Contact must be 10-15 digits")
        return value
    
    def validate_email(self, value):
        """
        Check if email already exists (for create operation)
        """
        # instance None means CREATE operation
        if self.instance is None:
            if Doctor.objects.filter(email=value).exists():
                raise serializers.ValidationError("Doctor with this email already exists")
        else:
            # Check if email changed and new email already exists
            if Doctor.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Doctor with this email already exists")
        
        return value
        