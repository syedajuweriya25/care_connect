from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            'full_name',
            'email',
            'phone',
            'role',
            'password',
            'password_confirm',
            'role_details',
            'blood_group',
            'emergency_contact_name',
            'emergency_contact_phone',
            'medical_conditions',
            'allergies',
            'address',
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value

    def validate_phone(self, value):
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) != 10:
            raise serializers.ValidationError('Phone number must contain exactly 10 digits.')
        return value

    def validate_role_details(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError('Role-specific details must be provided.')
        if not value:
            raise serializers.ValidationError('Role-specific details are required.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})

        if not attrs.get('role_details'):
            raise serializers.ValidationError({'role_details': 'Role-specific information is required.'})

        if not attrs.get('blood_group'):
            raise serializers.ValidationError({'blood_group': 'Blood group is required.'})
        if not attrs.get('emergency_contact_name'):
            raise serializers.ValidationError({'emergency_contact_name': 'Emergency contact name is required.'})

        emergency_contact_phone = attrs.get('emergency_contact_phone', '')
        digits = ''.join(filter(str.isdigit, emergency_contact_phone))
        if len(digits) != 10:
            raise serializers.ValidationError({'emergency_contact_phone': 'Emergency contact number is invalid.'})
        if not attrs.get('address'):
            raise serializers.ValidationError({'address': 'Address is required.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError({'detail': 'Invalid email or password.'})
        if not user.is_active:
            raise serializers.ValidationError({'detail': 'User account is inactive.'})
        attrs['user'] = user
        return attrs


class TokenObtainSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
            'role': self.user.role,
            'is_verified': self.user.is_verified,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'email',
            'phone',
            'role',
            'blood_group',
            'emergency_contact_name',
            'emergency_contact_phone',
            'medical_conditions',
            'allergies',
            'address',
            'role_details',
            'is_verified',
            'created_at',
        )
        read_only_fields = ('id', 'created_at', 'is_verified')
