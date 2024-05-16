# Import necessary modules and classes from Django and Django REST framework
from rest_framework import serializers
from django.contrib.auth.models import User


# Define serializers for User model

# Serializer for user registration (sign up) with additional validation
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        # Set the model to User
        model = User
        # Specify the fields to include in the serialized representation
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

        # Define extra validation for specific fields
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
        }


# Serializer for displaying user information
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Set the model to User
        model = User
        # Specify the fields to include in the serialized representation
        fields = ('username', 'first_name', 'last_name', 'email')




# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Customize the response data if needed
        return data