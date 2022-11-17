from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets,permissions,authentication,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from PMA_api.serializers import (
    UserSerializer,RegisterSerializer,PasswordsSerializer
)
from PMA_api.models import(
    Passwords,
)
from PMA.utils import get_object_or_None

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions
    ]
    authentication_classes = [authentication.TokenAuthentication]
    

class ListUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [ 
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
    ]

    def get(self, request, format=None):
        users = UserSerializer(User, many = True).data
        return Response(users)
  
    
class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]
    serializer_class = RegisterSerializer
  
    
class SignInUser(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get_or_create(user=user)[0]
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    
    
class PasswordView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [ 
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
    ]
    queryset = Passwords.objects.all()
    
    def post(self,request, *args, **kwargs):
        instance = get_object_or_None(self.queryset,id=kwargs.get('pk'))
        serializer = PasswordsSerializer(data = request.data,instance=instance)
        if serializer.is_valid(raise_exception=False):
            password = serializer.save(user=request.user)
            return Response(serializer.data) 
        print(serializer.errors)
        return Response(serializer.errors)
    
    def get(self,request, *args, **kwargs):
        instance = get_object_or_None(self.queryset,id=kwargs.get('pk'))
        serializer = PasswordsSerializer(instance,many=False)
        if instance is None:
            serializer = PasswordsSerializer(self.get_queryset(),many=True)
        
        return Response(serializer.data) 
    
    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)