
import threading
import requests

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LoginHistory, env_token


def send_sms(instance_id):

    try:
        # ==========================================
        # GET LOGIN HISTORY
        # ==========================================

        instance = LoginHistory.objects.select_related(
            "user"
        ).get(id=instance_id)

        # ==========================================
        # GET MOCEAN TOKEN
        # ==========================================

        token_obj = env_token.objects.first()

        if not token_obj:
            print("❌ Mocean token not found.")
            return

        token = token_obj.moceanapi_token

        if not token:
            print("❌ Mocean token is empty.")
            return

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
        # SMS MESSAGE
        # ==========================================

        message = (
            "LOGIN ALERT\n"
            "================\n"
            f"Name: {full_name}\n"
            f"Email: {instance.email or 'Unknown'}\n"
            f"IP: {instance.ip_address or 'Unknown'}\n"
            f"City: {instance.city or 'Unknown'}\n"
            f"Latitude: {instance.latitude or 'Unknown'}\n"
            f"Longitude: {instance.longitude or 'Unknown'}\n"
            f"Login Time: "
            f"{instance.login_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # ==========================================
        # MOCEAN API
        # ==========================================

        url = "https://rest.moceanapi.com/rest/2/sms"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": (
                "application/x-www-form-urlencoded"
            ),
        }

        data = {
            "mocean-from": "MOCEAN",
            "mocean-to": "8801323915030",
            "mocean-text": message,
        }

        # ==========================================
        # SEND SMS
        # ==========================================

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=10,
        )

        print(
            "Mocean Status:",
            response.status_code,
        )

        print(
            "Mocean Response:",
            response.text,
        )

    except requests.RequestException as e:

        print(
            "❌ SMS Request Error:",
            repr(e),
        )

    except Exception as e:

        print(
            "❌ SMS Error:",
            repr(e),
        )


# ==================================================
# LOGIN HISTORY SIGNAL
# ==================================================

@receiver(
    post_save,
    sender=LoginHistory,
)
def send_login_sms(
    sender,
    instance,
    created,
    **kwargs,
):

    # Only newly created LoginHistory
    if not created:
        return

    print(
        "🔥 LoginHistory created:",
        instance.id,
    )

    # ==============================================
    # BACKGROUND SMS THREAD
    # ==============================================

    thread = threading.Thread(
        target=send_sms,
        args=(instance.id,),
        daemon=True,
    )

    thread.start()

    print("📤 SMS thread started.")

