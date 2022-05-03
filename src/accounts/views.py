from django.shortcuts import render
from django.views import View

from rest_framework.views import APIView
from rest_framework import status

from accounts.authentication import create_access_token, create_refresh_token
from accounts.models import User

from.response import Response
from .serializers import UserLoginSerializer, UserSignupSerializer


class HomeView(View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "home.html"
        self.args = {}
        self.content = {}
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, self.args)

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
            refresh_token = create_access_token(login_user.id)
            response = Response(self.payload)
            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
            response.data = {
                "token":access_token
            }
            
            return response
