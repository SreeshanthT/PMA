from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from PMA_api.models import (
    Passwords,SharePassword
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name','last_name']
         
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class PasswordsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    
    # def __init__(self, ext=None, *args, **kwargs):
    #     if ext in self.Meta.fields:
    #         self.Meta.fields.remove(ext)
    #     super(PasswordsSerializer, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Passwords
        fields = ['id','platform', 'password','active','created_on','user']
        
class SharePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePassword
        fields = ["shareto", "password"]
        
class SharePasswordListSerializer(serializers.ModelSerializer):
    shareto = UserSerializer(read_only = True)
    password = PasswordsSerializer(read_only = True)
    class Meta:
        model = SharePassword
        fields = ["shareto", "password"]
        