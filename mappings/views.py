from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PatientDoctorMapping
from .serializers import (
    PatientDoctorMappingSerializer,
    PatientDoctorMappingCreateSerializer,
    PatientDoctorMappingListSerializer
)
from patients.models import Patient

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient-Doctor Mapping CRUD operations
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return mappings for patients created by current user only

        """
        # Get patient IDs created by current user
        user_patient_ids = Patient.objects.filter(
            created_by=self.request.user
        ).values_list('id', flat=True)
        
        # Filter mappings by those patient IDs
        return PatientDoctorMapping.objects.filter(
            patient_id__in=user_patient_ids
        )
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'create':
            return PatientDoctorMappingCreateSerializer
        elif self.action == 'list':
            return PatientDoctorMappingListSerializer
        return PatientDoctorMappingSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create new patient-doctor mapping

        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return detailed response with full mapping info
        mapping = serializer.instance
        detail_serializer = PatientDoctorMappingSerializer(mapping)
        
        return Response({
            'mapping': detail_serializer.data,
            'message': 'Doctor assigned to patient successfully'
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """
        Remove doctor from patient
        """
        instance = self.get_object()
        patient_name = instance.patient.name
        doctor_name = instance.doctor.name
        
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Dr. {doctor_name} removed from patient {patient_name}'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def by_patient(self, request, patient_id=None):
        """
        Get all doctors assigned to a specific patient
        
        URL: GET /api/mappings/patient/1/
        
        Returns: List of all doctors for patient ID 1
        """
        # Check if patient exists and belongs to current user
        try:
            patient = Patient.objects.get(
                id=patient_id,
                created_by=request.user
            )
        except Patient.DoesNotExist:
            return Response({
                'error': 'Patient not found or you do not have permission'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get all mappings for this patient
        mappings = self.get_queryset().filter(patient_id=patient_id)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        
        return Response({
            'patient': {
                'id': patient.id,
                'name': patient.name
            },
            'doctors': serializer.data,
            'count': mappings.count()
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active mappings
        
        URL: GET /api/mappings/active/
        """
        active_mappings = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_mappings, many=True)
        
        return Response({
            'mappings': serializer.data,
            'count': active_mappings.count()
        }, status=status.HTTP_200_OK)