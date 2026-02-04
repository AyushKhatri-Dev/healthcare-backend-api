from rest_framework.routers import DefaultRouter
from .views import PatientDoctorMappingViewSet

router = DefaultRouter()
router.register('', PatientDoctorMappingViewSet, basename='mapping')
urlpatterns = router.urls