# Import necessary modules
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ContactMessageSerializer
from .models import ContactMessage
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


# Define an API view for creating a contact message
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  # Ensure the user is authenticated
# @throttle_classes([UserRateThrottle])  # Apply rate throttling
# def contact_message_create(request):
#     # Prepare data for the contact message
#     data = {
#         'name': request.data.get('name'),
#         'email': request.user.email,  # Use the authenticated user's email
#         'message': request.data.get('message'),
#     }
#
#     # Create a serializer instance with the provided data and context
#     serializer = ContactMessageSerializer(data=data, context={'request': request})
#
#     # Validate the serializer data
#     if serializer.is_valid():
#         # Save the valid data as a new contact message
#         serializer.save()
#         return Response({"message": "Your message has been sent successfully. Thank you for contacting us."},
#                         status=status.HTTP_201_CREATED)
#
#     # If validation fails, return errors with a bad request status
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def contact_message_create(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Prepare data for the contact message using the authenticated user's email
        data = {
            'name': request.data.get('name', ''),
            'email': request.user.email,
            'message': request.data.get('message', ''),
        }
    else:
        # For non-authenticated users, require all fields in the request data
        data = {
            'name': request.data.get('name', ''),
            'email': request.data.get('email', ''),
            'message': request.data.get('message', ''),
        }

        # Ensure that all fields are provided for unauthenticated users
        if not all(data.values()):
            return Response({'error': 'All fields are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

    # Create a serializer instance with the provided data and context
    serializer = ContactMessageSerializer(data=data, context={'request': request})

    # Validate the serializer data
    if serializer.is_valid():
        # Save the valid data as a new contact message
        serializer.save()
        return Response({"message": "Your message has been sent successfully. Thank you for contacting us."},
                        status=status.HTTP_201_CREATED)

    # If validation fails, return errors with a bad request status
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define an API view for retrieving messages for the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def user_messages(request):
    # Retrieve messages for the authenticated user based on their email
    user_email = request.user.email
    messages = ContactMessage.objects.filter(email=user_email)

    # Serialize the messages using the ContactMessageSerializer
    serializer = ContactMessageSerializer(messages, many=True)

    # Return a response with the serialized messages and a success status
    return Response({'Your messages': serializer.data}, status=status.HTTP_200_OK)


def admin_messages(request):
    messages = ContactMessage.objects.all()
    return render(request, 'admin_dashboard.html', {'messages': messages})


from django.http import JsonResponse
from .models import ContactMessage


def admin_messages_count(request):
    user_email = request.user.email
    new_messages_count = ContactMessage.objects.filter(email=user_email, is_read=False).count()
    return JsonResponse({'new_messages_count': new_messages_count})
