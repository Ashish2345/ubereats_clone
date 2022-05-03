from django.contrib.auth import authenticate
from datetime import datetime

from .models import User

from rest_framework import serializers


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email", "contact_no", "dob", 
            "gender", "password"
        ]
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def __init__(self, *args, **kwargs):
        super(self.__class__,self).__init__(*args, **kwargs)
        field_names = [field_names for field_names, _ in self.fields.items()]
        for field_name in field_names:
            field = self.fields.get(field_name)
            if field.read_only is False:
                field.allow_null = False
                field.required = True

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        if data["dob"] > datetime.today():
            raise serializers.ValidationError("Date of birth cannot be above today's data")
        return data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        querset = User.objects.filter(email=data.get("email", None))
        if not querset:
            raise serializers.ValidationError("Email is not registered!!")
        if authenticate(email=data["email"], password=data.get('password', None)) is None:
            raise serializers.ValidationError("Email or password is incorrect")
        return super().validate(data)