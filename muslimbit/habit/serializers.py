from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        validators=[validate_password],
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'username')

    def create(self, validated_data):
        print("validated Data:", validated_data)  # Debugging

        user = User.objects.create(

            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        
        # Add the user object to validated_data
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

    bio = serializers.CharField(source='profile.bio', read_only=True)
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']

    def update(self, instance, validated_data):
        print("Incoming Data:", validated_data)

        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # Handle bio field if it exists in validated_data
        bio = validated_data.get('bio')
        if bio is not None:
            instance.profile.bio = bio

        # Handle profile_picture field if it exists in validated_data
        profile_picture = validated_data.get('profile_picture')
        if profile_picture is not None:
            instance.profile.profile_picture = profile_picture

        # Save the profile after updating
        instance.profile.save()

        return instance
    
        
    
class UserProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio', required=False)
    profile_picture = serializers.ImageField(source='profile.profile_picture', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']

    def update(self, instance, validated_data):
        # Debugging to inspect incoming data
        print("Incoming Data:", validated_data)

        # Extract profile data (nested under 'profile')
        profile_data = validated_data.pop('profile', {})

        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # Update profile fields
        profile = instance.profile  # Ensure the Profile exists
        profile.bio = profile_data.get('bio', profile.bio)
        profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
        profile.save()

        return instance
