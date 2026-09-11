from django.db import models
from django.db import models
from django.contrib.auth.models import User

class env_token(models.Model):
    gemini_token = models.CharField(max_length=255)
    moceanapi_token = models.CharField(max_length=255)

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    username = models.CharField(max_length=150)
    email = models.EmailField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    login_time = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username} - {self.login_time}"

import os
import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=LoginHistory)
def send_login_sms(sender, instance, created, **kwargs):

   
    if not created:
        return


    url = "https://rest.moceanapi.com/rest/2/sms"
    token = env_token.objects.first().moceanapi_token  # Get the token from the database
    headers = {
        "Authorization": (
            f"Bearer {token}"
        ),
        "Content-Type": "application/x-www-form-urlencoded",
    }

    
    
    message = (
        f"Login Alert!\n"
        f"User: {instance.username}\n"
        f"IP: {instance.ip_address}\n"
        f"Location: {instance.city}, {instance.country}\n"
        f"Name: {instance.user.first_name} {instance.user.last_name}\n"
        f"Email: {instance.user.email}\n"
        f"Login Time: {instance.login_time.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    data = {
        "mocean-from": "MOCEAN",
        "mocean-to": "8801323915030",  # Replace with the actual recipient number
        "mocean-text": message,
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=10
        )

        print("Mocean Response:", response.text)

    except requests.RequestException as e:

        print("SMS Error:", e)

class Students(models.Model):

    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    
    # Academic Information
    semester = models.IntegerField()
    roll = models.IntegerField(unique=True)
    reg = models.IntegerField(unique=True)
    session = models.CharField(max_length=20)
    shift = models.CharField(max_length=10, choices=[('Morning', 'Morning'), ('Day', 'Day')])
    section = models.CharField(max_length=5,blank=True,null=True)
    
    # Contact Information
    mobile_number = models.CharField(max_length=15)
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    present_address = models.TextField()
    permanent_address = models.TextField()
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)
    
    # Other Information
    nationality = models.CharField(max_length=50, default='Bangladeshi')
    religion = models.CharField(max_length=30, blank=True, null=True)

    
    # Photo
    profile_picture = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    
class Additional_information(models.Model):
    login_page_image = models.ImageField(upload_to="login_page_image/")