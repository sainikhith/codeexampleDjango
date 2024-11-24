# utils.py
import pyotp
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def generate_otp(user_email):
    try:
        # Generate OTP using pyotp
        totp = pyotp.TOTP('base32secret3232', interval=10)  # Use a secure secret
        otp = totp.now()

        # Send OTP via email to the user
        subject = "Your OTP Code"
        message = f"Hello, here is your OTP: {otp}"
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [user_email])
        return otp
    except Exception as e:
        raise e  # Re-raise the exception for higher-level handling
