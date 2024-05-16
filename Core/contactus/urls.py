# Import necessary modules
from django.urls import path
from . import views  # Import views module from the same directory

# Define URL patterns using the path() function
urlpatterns = [
    # Define a URL pattern for the 'contact-message/' endpoint
    path('contact_message/', views.contact_message_create, name='contact_message'),

    # Define a URL pattern for the 'user-messages/' endpoint
    path('user_messages/', views.user_messages, name='user_messages'),
    path('admin/customer_messages/', views.admin_messages, name='admin_messages'),
    path('admin/messages/count/', views.admin_messages_count, name='admin_messages_count'),

]
