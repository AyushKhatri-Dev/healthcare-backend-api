from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer, PatientCreateUpdateSerializer

class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient CRUD operations
    
    Automatically provides:
    - POST   /api/patients/         → create()
    - GET    /api/patients/         → list()
    - GET    /api/patients/{id}/    → retrieve()
    - PUT    /api/patients/{id}/    → update()
    - PATCH  /api/patients/{id}/    → partial_update()
    - DELETE /api/patients/{id}/    → destroy()
    """
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated]  # Only logged-in users
    
    def get_queryset(self):
        """
        Return patients created by current user only
        """
        return Patient.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action in ['create', 'update', 'partial_update']:
            return PatientCreateUpdateSerializer
        return PatientSerializer
    
    def perform_create(self, serializer):
        """
        Custom logic during creation

        """
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to add custom response message
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return response with custom message
        return Response({
            'patient': PatientSerializer(serializer.instance).data,
            'message': 'Patient created successfully'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to add custom response message
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'patient': PatientSerializer(serializer.instance).data,
            'message': 'Patient updated successfully'
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to add custom response message
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'message': 'Patient deleted successfully'
        }, status=status.HTTP_200_OK)