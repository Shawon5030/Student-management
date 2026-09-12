from django.db import models
from django.db import models
from django.contrib.auth.models import User

class env_token(models.Model):
    gemini_token = models.CharField(max_length=255)
    moceanapi_token = models.CharField(max_length=255)

from django.db import models
from django.contrib.auth.models import User


class LoginHistory(models.Model):

    # =========================
    # USER INFORMATION
    # =========================

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    username = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    # =========================
    # IP
    # =========================

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    hostname = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # =========================
    # LOCATION
    # =========================

    country = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    country_code = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    region = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    region_code = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    postal_code = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    # =========================
    # COORDINATES
    # =========================

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    # =========================
    # NETWORK
    # =========================

    isp = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    organization = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    asn = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    network = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # =========================
    # TIME
    # =========================

    timezone = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    utc_offset = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    # =========================
    # COUNTRY INFORMATION
    # =========================

    continent_code = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    currency = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    currency_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    languages = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    calling_code = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    in_eu = models.BooleanField(
        null=True,
        blank=True
    )

    # =========================
    # COMPLETE IPINFO RESPONSE
    # =========================

    ipinfo_data = models.JSONField(
        null=True,
        blank=True
    )

    # =========================
    # LOGIN TIME
    # =========================

    login_time = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username} - {self.login_time}"


import requests

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LoginHistory, env_token


@receiver(
    post_save,
    sender=LoginHistory
)
def send_login_sms(
    sender,
    instance,
    created,
    **kwargs
):

    # Only newly created LoginHistory
    if not created:
        return

    try:

        # ==========================================
        # GET SMS.BD API KEY
        # ==========================================

        token_obj = env_token.objects.first()

        if not token_obj:
            print("SMS.bd API key not found.")
            return

        api_key = token_obj.moceanapi_token

        if not api_key:
            print("SMS.bd API key is empty.")
            return

        # ==========================================
        # SMS.BD API
        # ==========================================

        url = "https://api.sms.net.bd/sendsms"

        # ==========================================
        # USER
        # ==========================================

        user = instance.user

        full_name = (
            f"{user.first_name or ''} "
            f"{user.last_name or ''}"
        ).strip()

        if not full_name:
            full_name = "Unknown"

        # ==========================================
        # IPINFO COMPLETE DATA
        # ==========================================

        ipinfo_data = instance.ipinfo_data or {}

        # ==========================================
        # BASIC INFORMATION
        # ==========================================

        message = (
            "LOGIN ALERT\n"
            "================\n"
            f"Username: "
            f"{instance.username or 'Unknown'}\n"

            f"Name: "
            f"{full_name}\n"

            f"Email: "
            f"{instance.email or 'Unknown'}\n"

            f"User ID: "
            f"{user.id}\n\n"

            f"IP: "
            f"{instance.ip_address or 'Unknown'}\n"



            f"Latitude: "
            f"{instance.latitude or 'Unknown'}\n"

            f"Longitude: "
            f"{instance.longitude or 'Unknown'}\n\n"

            f"Login Time: "
            f"{instance.login_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # ==========================================
        # COMPLETE IPINFO DATA
        # ==========================================

        if ipinfo_data:

            message += (
                "\n\n"
                "IPINFO DATA\n"
                "================\n"
            )

            for key, value in ipinfo_data.items():

                # Avoid duplicate fields
                if key in [
                    "ip",
                    "city",
                    "region",
                    "postal",
                ]:
                    continue

                message += (
                    f"{key}: {value}\n"
                )

        # ==========================================
        # SMS.BD DATA
        # ==========================================

        data = {
            "api_key": api_key,
            "msg": message,
            "to": "8801323915030",
        }

        # ==========================================
        # SEND SMS
        # ==========================================

        response = requests.post(
            url,
            data=data,
            timeout=10
        )

        print(
            "SMS.bd Status:",
            response.status_code
        )

        print(
            "SMS.bd Response:",
            response.text
        )

    except requests.RequestException as e:

        print(
            "SMS.bd Request Error:",
            e
        )

    except Exception as e:

        print(
            "SMS.bd Error:",
            e
        )


        
        
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