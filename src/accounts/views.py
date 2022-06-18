import datetime
from distutils.log import error

from rest_framework.views import APIView
from rest_framework import status
from yaml import serialize


from accounts.authentication import (JWTAuthentication, create_access_token, create_refresh_token, 
                                    decode_access_token, decode_refresh_token)
from accounts.models import User, UserToken

from.response import Response
from .serializers import (UserLoginSerializer,  UserSignupSerializer, UserSerializer)


class RegisterAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        self.payload = {}
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serailizers = UserSignupSerializer(data=request.data)
        if serailizers.is_valid():
            serailizers.save()
            self.payload['message'] = 'User is successfully registered'
            return Response(self.payload, status=status.HTTP_200_OK)
        return Response(self.payload, errors=serailizers.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        self.payload = {}
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serailizers = UserLoginSerializer(data=request.data)
        if serailizers.is_valid():
            self.payload['message'] = 'User is successfully logged in!!'
            login_user = User.objects.get(email=request.data['email'])
            access_token = create_access_token(login_user.id)
            refresh_token = create_refresh_token(login_user.id)

            response = Response()
            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
            response.data = {
                "access_token":access_token
            }
            return response


class       UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def dispatch(self, request, *args, **kwargs):
        self.payload = {}
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):  
        self.payload['user_details'] = UserSerializer(request.user).data
        return Response(self.payload, status=status.HTTP_200_OK)

class RefreshAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        self.payload = {}
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)
        qs = UserToken.objects.filter(user_id=id, token = refresh_token, exipired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)).exists()
        if qs: 
            access_token = create_access_token(id)
            self.payload["refresh_token"] = access_token
            return Response(self.payload, status=status.HTTP_200_OK)
        return Response(self.payload, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        UserToken.objects.filter(token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': "Logged Out"
        }
        return response 