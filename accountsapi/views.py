from accountsapi.serializers import LoginSerializer, ProfileSerializer, RegisterSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate


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

    # user = User.objects.filter(username=username).first()
    # if user and user.check_password(password):
    #     return Response({
    #         "status": True,
    #         "data": {'token' : str(Token.objects.get_or_create(user=user)[0].key)}
    #     })

    user_obj = authenticate(username=username, password=password)
    if user_obj:
        return Response({
            "status": True,
            "data": {'token' : str(Token.objects.get_or_create(user=user_obj)[0].key)}
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
            return Response({
                "status": True,
                "message": "User Created Successfully",
                "data" : serializer.data
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