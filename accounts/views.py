from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

class RegisterView(APIView):
    """
    API endpoint for user registration
    
    URL: POST /api/auth/register/
    Permission: Anyone can register (no authentication required)
    """
    
    permission_classes = [AllowAny]  # No authentication required
    
    def post(self, request):
        """
        Handle POST request for registration
        
        Input (request.data):
        {
            "name": "Ayush Khatri",
            "email": "ayush@example.com",
            "password": "password123",
            "password2": "password123"
        }
        
        Output:
        {
            "user": {...},
            "message": "User registered successfully"
        }
        """
        
        # Create serializer instance with request data
        serializer = UserRegistrationSerializer(data=request.data)
        
        # Validate data
        if serializer.is_valid():
            # Save user to database
            user = serializer.save()
            
            # Return success response
            return Response({
                'user': UserSerializer(user).data,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        
        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login with JWT token generation
    
    URL: POST /api/auth/login/
    Permission: Anyone can login (no authentication required)
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle POST request for login
        
        Input (request.data):
        {
            "email": "ayush@example.com",
            "password": "password123"
        }
        
        Output:
        {
            "user": {...},
            "access": "eyJhbGci...",  // Access token (1 hour validity)
            "refresh": "eyJhbGci...", // Refresh token (1 day validity)
            "message": "Login successful"
        }
        """
        
        # Get email and password from request
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Validate input
        if not email or not password:
            return Response({
                'error': 'Please provide both email and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # User authenticated successfully
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),  # Access token
                'refresh': str(refresh),              # Refresh token
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            # Invalid credentials
            return Response({
                'error': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)