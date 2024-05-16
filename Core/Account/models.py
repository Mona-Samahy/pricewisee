# Import necessary modules and classes from Django
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Define your models here.

# Create a model named 'Profile' to store additional user-related information
class Profile(models.Model):
    # Define a one-to-one relationship with the built-in User model in Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Store a token for resetting the password, with a maximum length of 50 characters
    reset_password_token = models.CharField(max_length=50, default="", blank=True)

    # Store the expiration date and time for the password reset token
    reset_password_expire = models.DateTimeField(null=True, blank=True)


# Define a signal receiver function to create a Profile instance when a User instance is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    # Get the User instance
    user = instance

    # Check if the User instance was just created
    if created:
        # If created, create a corresponding Profile instance and save it
        profile = Profile(user=user)
        profile.save()
