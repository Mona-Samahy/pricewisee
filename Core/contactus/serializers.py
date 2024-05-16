# Import necessary modules
from rest_framework import serializers
from django.core.validators import EmailValidator  # Import EmailValidator for email field validation
from django.contrib.auth import get_user_model
from .models import ContactMessage


# Define a UserSerializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model for the serializer
        model = get_user_model()
        # Specify the fields to include in the serialization
        fields = ['username']


# Define a ContactMessageSerializer for the ContactMessage model
class ContactMessageSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=not serializers.CurrentUserDefault())

    class Meta:
        # Specify the model for the serializer
        model = ContactMessage
        # Specify the fields to include in the serialization
        fields = ['name', 'email', 'message', 'created_at']
