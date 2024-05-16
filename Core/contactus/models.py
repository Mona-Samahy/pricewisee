# Import necessary modules
from django.db import models
from django.contrib.auth.models import User


# Define the ContactMessage model
class ContactMessage(models.Model):
    # Define a CharField for the 'name' attribute with a maximum length of 100 characters
    name = models.CharField(max_length=100)

    # Define an EmailField for the 'email' attribute
    email = models.EmailField()

    # Define a TextField for the 'message' attribute
    message = models.TextField()

    # Define a DateTimeField for the 'created_at' attribute with auto_now_add set to True
    created_at = models.DateTimeField(auto_now_add=True)

    # Define a ForeignKey relationship with the User model, allowing a message to be associated with a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Define metadata for the model
    class Meta:
        # Specify the plural name for the model in the admin interface
        verbose_name_plural = 'Client messages'
