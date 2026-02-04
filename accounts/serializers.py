from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration

    """
    password2 = serializers.CharField(
        write_only = True,
        required = True,
        style= {'input_type', 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only': True},
            'id': {'read_only': True}
        }

    def validate(self, attrs):
        """
        Custom validation method
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "password fields didn't match."
            })

        validate_password(attrs['password'])

        return attrs

    def create(self, validated_data):
        """
        Create new user with hashed password
        """
        validated_data.pop('password2')

        #create user with hashed password
        user = User.objects.create_user(
            email=validated_data['email'],
            username = validated_data['email'],
            name=validated_data['name'],
            password= validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    # Response Field
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for displaying user info
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'date_joined']
        read_only_fields = ['id', 'date_joined']
