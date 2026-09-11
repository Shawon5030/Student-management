import json
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
        # GET MOCEAN TOKEN
        # ==========================================

        token_obj = (
            env_token.objects.first()
        )

        if not token_obj:

            print(
                "Mocean token not found."
            )

            return

        token = (
            token_obj.moceanapi_token
        )

        if not token:

            print(
                "Mocean token is empty."
            )

            return

        # ==========================================
        # MOCEAN API
        # ==========================================

        url = (
            "https://rest.moceanapi.com/rest/2/sms"
        )

        headers = {
            "Authorization": (
                f"Bearer {token}"
            ),
            "Content-Type": (
                "application/x-www-form-urlencoded"
            ),
        }

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

        ipinfo_data = (
            instance.ipinfo_data or {}
        )

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

            f"Hostname: "
            f"{instance.hostname or 'Unknown'}\n\n"

            f"Country: "
            f"{instance.country or 'Unknown'} "
            f"({instance.country_code or 'N/A'})\n"

            f"Region: "
            f"{instance.region or 'Unknown'}\n"

            f"City: "
            f"{instance.city or 'Unknown'}\n"

            f"Postal: "
            f"{instance.postal_code or 'Unknown'}\n"

            f"Latitude: "
            f"{instance.latitude or 'Unknown'}\n"

            f"Longitude: "
            f"{instance.longitude or 'Unknown'}\n\n"

            f"Organization: "
            f"{instance.organization or 'Unknown'}\n"

            f"Timezone: "
            f"{instance.timezone or 'Unknown'}\n\n"

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

            for key, value in (
                ipinfo_data.items()
            ):

                # Avoid duplicate huge fields
                if key in [
                    "ip",
                    "hostname",
                    "city",
                    "region",
                    "country",
                    "postal",
                    "timezone",
                    "org",
                ]:
                    continue

                message += (
                    f"{key}: {value}\n"
                )

        # ==========================================
        # SMS DATA
        # ==========================================

        data = {
            "mocean-from": "MOCEAN",

            "mocean-to": (
                "8801323915030"
            ),

            "mocean-text": message,
        }

        # ==========================================
        # SEND SMS
        # ==========================================

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=10
        )

        print(
            "Mocean Status:",
            response.status_code
        )

        print(
            "Mocean Response:",
            response.text
        )

    except requests.RequestException as e:

        print(
            "SMS Request Error:",
            e
        )

    except Exception as e:

        print(
            "SMS Error:",
            e
        )