# Import necessary modules
from django.contrib import admin
from .models import ContactMessage


# Create a custom admin class for the ContactMessage model
class ContactMessageAdmin(admin.ModelAdmin):
    # Specify the fields to be displayed in the list view
    list_display = ['name', 'email', 'message', 'created_at']

    # Enable search functionality for specified fields in the list view
    search_fields = ['name', 'email', 'message']

    # Specify the fields to be displayed in the detail view/edit form
    fields = ['name', 'email', 'message', 'created_at']

    # Disable clickable links for all fields in the list view
    list_display_links = None


# Register the ContactMessage model with the custom admin class
admin.site.register(ContactMessage, ContactMessageAdmin)
