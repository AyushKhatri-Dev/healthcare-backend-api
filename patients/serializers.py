from rest_framework import serializers
from .models import Patient
from accounts.serializers import UserSerializer

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for patient model
    """
    created_by = UserSerializer(read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'age',
            'gender',
            'gender_display',  
            'contact',
            'address',
            'medical_history',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate_contact(self, value):
        """
        Validate contact number
        """
        if not value.isdigit():
            raise serializers.ValidationError("Contact must contain only digits")
        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Contact must be 10-15 digits")
        return value

class PatientCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Separate serializer for create/update operations
    """
    class Meta:
        model = Patient
        fields = [
            'name',
            'age',
            'gender',
            'contact',
            'address',
            'medical_history'
        ]

    def validate_age(self, value):
        if value < 0 or value > 150:
            raise serializers.ValidationError("Age must be between 0 and 150")
        return value

    def validate_contact(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Contact must contain only digits")
        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Contact must be 10-15 digits")
        return value