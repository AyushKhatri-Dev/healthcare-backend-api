from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient-Doctor Mapping
    
    Shows complete details with nested patient and doctor info
    """
    # Nested serializers for complete information
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only = True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id',
            'patient',
            'doctor',
            'assigned_date',
            'notes',
            'is_active'
        ]
        read_only_fields = ['id', 'assigned_date']

class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating mappings
    
    Takes only IDs, not full objects
    """

    patient_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient_id', 'doctor_id', 'notes', 'is_active']
        read_only_fields = ['id']

    def validate_patient_id(self, value):
        """
        Check if patient exists
        """
        from patients.models import Patient
        
        if not Patient.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Patient with ID {value} does not exist")

        return value

    def validate_doctor_id(self, value):
        """
        Check if doctor exists
        """
        from doctors.models import Doctor

        if not Doctor.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Patient with ID {value} does not exist")
        return value

    def validate(self, attrs):
        """
        Object-level validation
        
        Check if mapping already exists
        """
        from patients.models import Patient
        from doctors.models import Doctor

        patient_id = attrs.get('patient_id')
        doctor_id = attrs.get('doctor_id')

        # Check if patient belongs to current user
        patient = Patient.objects.filter(id=patient_id).first()
        request = self.context.get('request')

        if patient and request and patient.created_by != request.user:
            raise serializers.ValidationError({
                "patient_id": "You can only assign your own patients to doctors"
            })

        # Check if mapping already exists
        if PatientDoctorMapping.objects.filter(
            patient_id=patient_id,
            doctor_id=doctor_id
        ).exists():
            raise serializers.ValidationError(
                "This patient is already assigned to this doctor"
            )

        return attrs

    def create(self, validated_data):
        """
        Create mapping with patient and doctor objects
        """
        from patients.models import Patient
        from doctors.models import Doctor
        
        # Get IDs
        patient_id = validated_data.pop('patient_id')
        doctor_id = validated_data.pop('doctor_id')
        
        # Get actual objects
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Create mapping
        mapping = PatientDoctorMapping.objects.create(
            patient=patient,
            doctor=doctor,
            **validated_data
        )
        
        return mapping

class PatientDoctorMappingListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing mappings
    
    Shows basic info without nested details
    """
    
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_id = serializers.IntegerField(source='patient.id', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_id = serializers.IntegerField(source='doctor.id', read_only=True)
    doctor_specialization = serializers.CharField(
        source='doctor.get_specialization_display', 
        read_only=True
    )
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id',
            'patient_id',
            'patient_name',
            'doctor_id',
            'doctor_name',
            'doctor_specialization',
            'assigned_date',
            'is_active'
        ]


