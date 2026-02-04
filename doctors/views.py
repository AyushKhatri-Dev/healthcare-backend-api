from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Doctor CRUD operations
    
    Automatically provides:
    - POST   /api/doctors/         → create()
    - GET    /api/doctors/         → list()
    - GET    /api/doctors/{id}/    → retrieve()
    - PUT    /api/doctors/{id}/    → update()
    - PATCH  /api/doctors/{id}/    → partial_update()
    - DELETE /api/doctors/{id}/    → destroy()
    
    Note: Doctors are NOT user-specific (no filtering by created_by)
    Any authenticated user can view/manage all doctors
    """
    
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """
        Create new doctor with custom response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'doctor': serializer.data,
            'message': 'Doctor added successfully'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Update doctor with custom response
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'doctor': serializer.data,
            'message': 'Doctor updated successfully'
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete doctor with custom response
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'message': 'Doctor deleted successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Custom endpoint to get only available doctors
        
        URL: GET /api/doctors/available/
        
        Returns: List of doctors where available=True
        """
        available_doctors = self.queryset.filter(available=True)
        serializer = self.get_serializer(available_doctors, many=True)
        
        return Response({
            'doctors': serializer.data,
            'count': available_doctors.count()
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def by_specialization(self, request):
        """
        Custom endpoint to filter doctors by specialization
        
        URL: GET /api/doctors/by_specialization/?specialization=CARDIOLOGY
        
        Query Parameter: specialization (CARDIOLOGY, NEUROLOGY, etc.)
        """
        specialization = request.query_params.get('specialization', None)
        
        if not specialization:
            return Response({
                'error': 'Please provide specialization parameter'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        doctors = self.queryset.filter(specialization=specialization)
        serializer = self.get_serializer(doctors, many=True)
        
        return Response({
            'specialization': specialization,
            'doctors': serializer.data,
            'count': doctors.count()
        }, status=status.HTTP_200_OK)