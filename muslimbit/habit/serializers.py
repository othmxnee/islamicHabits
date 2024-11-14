from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import PasswordValidator
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.modelSerializer):
    email = serializers.EmailField(
        reqired=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        validators=[PasswordValidator()],
        write_only=True
    )
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name','username')
        
        def create(self, validated_data):
            user = User.objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                # password=validated_data["password"]
            )
            user.set_password(validated_data["password"])
            user.save()
            return user