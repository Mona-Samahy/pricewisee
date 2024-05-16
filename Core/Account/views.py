# Import necessary modules and classes
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
import secrets
from datetime import datetime, timedelta
from django.core.mail import send_mail


# Define a Django REST framework view for user registration
@api_view(['POST'])
def register(request):
    # Extract data from the request
    data = request.data

    # Validate user data using SignUpSerializer
    user = SignUpSerializer(data=data)
    if user.is_valid():
        # Check if username and email are unique
        if not User.objects.filter(username=data['username']).exists():
            if not User.objects.filter(email=data['email']).exists():
                # Create a new user with hashed password
                user = User.objects.create(
                    username=data['username'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=make_password(data['password'])
                )
                return Response({'details': 'Your account registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'This Email Already Exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'This Username Already Exist'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


# Define a Django REST framework view to get the current user information
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    # Serialize the current user data and return a response
    user = UserSerializer(request.user, many=False)
    return Response(user.data)


# Define a Django REST framework view to update user information
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    # Get the current user and data from the request
    user = request.user
    data = request.data

    # Update user attributes if provided, using the current values as defaults
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    # Check if the new username and email are unique
    if not User.objects.filter(username=user.username).exclude(pk=user.pk).exists():
        if not User.objects.filter(email=user.email).exclude(pk=user.pk).exists():
            # Save the updated user and return a success response
            user.save()
            return Response({'details': 'Your Data Updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This Email Already Exist'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'This Username Already Exist'}, status=status.HTTP_400_BAD_REQUEST)


def get_current_host(request):
    # Check if the request is made using a secure (HTTPS) connection
    protocol = request.is_secure() and 'https' or 'http'

    # Get the host (domain) from the request
    host = request.get_host()

    # Return the formatted URL with the current protocol and host
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


# Define a Django REST framework view that handles POST requests for password reset
@api_view(['POST'])
def forgot_password(request):
    # Extract the data (including email) from the request
    data = request.data

    # Check if a user with the provided email exists
    user_exists = User.objects.filter(email=data['email']).exists()

    if not user_exists:
        return Response({'error': 'User not found with the specified email'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve a user based on the provided email
    user = get_object_or_404(User, email=data['email'])

    # Generate a secure and random token (URL-safe base64-encoded string) for the password reset
    token = secrets.token_urlsafe(40)

    # Set an expiration date for the password reset link (30 minutes from the current time)
    expire_date = datetime.now() + timedelta(minutes=30)

    # Update the user's profile with the generated token and expiration date
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    # Get the current host (protocol and domain) from the request
    host = get_current_host(request)

    # Construct the reset password link with the generated token
    link = f"{host}api/reset_password/{token}"

    # Compose the email body with the reset password link
    body = f"Your Password Reset Link Is: {link}"

    # Send an email to the user with the reset password link
    send_mail(
        "Password Reset From FloorPlan",
        body,
        "mohaameedsaameer@gmail.com",
        [data['email']]
    )

    # Return a response indicating that the password reset email has been sent
    return Response({'details': f'Password reset sent to {data["email"]}'}, status=status.HTTP_200_OK)


# Define a Django REST framework view that handles POST requests for password reset
@api_view(['POST'])
def reset_password(request, token):
    # Extract data from the request
    data = request.data

    # Retrieve the user based on the provided reset password token
    user = get_object_or_404(User, profile__reset_password_token=token)

    # Check if the token has expired
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'Error': 'Token is Expired'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the entered passwords match
    if data['password'] != data['confirmPassword']:
        return Response({'Error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    # Set the new password using Django's make_password function
    user.password = make_password(data['password'])

    # Clear the reset password token and expiration date
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None

    # Save the changes to the user and user's profile
    user.profile.save()
    user.save()

    # Return a response indicating the successful password reset
    return Response({'details': 'Password reset successfully'})




