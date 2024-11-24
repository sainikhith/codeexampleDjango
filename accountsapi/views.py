from accountsapi.serializers import EmailOtpLoginSerializer, LoginSerializer, ProfileSerializer, RegisterSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from django.core.cache import cache

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate

from .utils import generate_otp
import pyotp

@swagger_auto_schema(method='post',request_body=LoginSerializer)
@api_view(['POST'])
def loginpost(request):
    serializer = LoginSerializer(data = request.data)
    if not serializer.is_valid():
        return Response({
            "status": False,
            "data": serializer.errors
        })
    username = serializer.data['username']
    password = serializer.data['password']

    user = User.objects.filter(username=username).first()
    # if user and user.check_password(password):
    #     return Response({
    #         "status": True,
    #         "data": {'token' : str(Token.objects.get_or_create(user=user)[0].key)}
    #     })
    user_obj = authenticate(username=username, password=password)
    user_data = {
        "id": user.id,
        "name": f"{user.first_name} {user.last_name}".strip() if user.first_name or user.last_name else user.username,
        "token": str(Token.objects.get_or_create(user=user_obj)[0].key),
    }
    if user_obj:
        return Response({
            "status": True,
            "data": user_data
        })

    return Response({
        "status": True,
        "data": {},
        "message": "Invalid Credentials"
    })


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = {
                "id": user.id,
                "username": user.username,
                "email" : getattr(user, "email", "")
            }
            return Response({
                "status": True,
                "message": "User Created Successfully",
                "data" : user_data
            }, status= status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        print(serializer.data)
        return Response({
            "status": True,
            "data": serializer.data
        })


# OTP-based Auth
# Step 1: Generate OTP for the given email
@api_view(['PUT'])
def generate_otp_for_email(request, email):
    # email = request.data.get("email")

    if not email:
        return Response({
            "status": False,
            "message": "Email is required"
        }, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            "status": False,
            "message": "User not found"
        }, status=404)
    except Exception as e:
        return Response({
            "status": False,
            "message": "An error occurred while retrieving the user."
        }, status=500)

    # Generate OTP and send it to the email
    try:
        # Generate OTP and send it to the email
        otp = generate_otp(email)
        # Store OTP in cache with a 5-minute expiration
        cache.set(f"otp_{email}", otp, timeout=300)
    except Exception as e:
        return Response({
            "status": False,
            "message": "Failed to generate or send OTP. Please try again later."
        }, status=500)
    
    return Response({
        "status": True,
        "message": f"The otp for user {user.username} has been sent to mail"
    }, status=200)


# Step 2: Verify OTP entered by the user
@swagger_auto_schema(method='post', request_body=EmailOtpLoginSerializer)
@api_view(['POST'])
def verify_otp_login(request):
    email = request.data.get("email")
    otp_provided = request.data.get("otp")

    if not email or not otp_provided:
        return Response({
            "status": False,
            "message": "Email and OTP are required"
        }, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            "status": False,
            "message": "User not found"
        }, status=404)

    # Retrieve the OTP from the cache
    cached_otp = cache.get(f"otp_{email}")
    print(cached_otp)
    if cached_otp is None:
        return Response({"status": False, "message": "OTP has expired or does not exist"}, status=400)

    if cached_otp == otp_provided:  # Check if the provided OTP matches
        # Successful login, return token
        token = str(Token.objects.get_or_create(user=user)[0].key)
        # Delete OTP from cache after successful verification
        cache.delete(f"otp_{email}")
        return Response({
            "status": True,
            "message": "Login successful",
            "data": {"token": token}
        })
    else:
        return Response({
            "status": False,
            "message": "Invalid OTP"
        }, status=400)