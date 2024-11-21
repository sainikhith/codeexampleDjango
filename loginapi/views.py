from loginapi.serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


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