from rest_framework import serializers
from .utils import *
from .models import *
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


def validate_password_no_spaces(value):
    if ' ' in value:
        raise ValidationError("Password should not contain spaces.")


def validate_not_only_spaces(value):
    if value.strip() == '':
        raise ValidationError("Field should not contain only spaces.")


def validate_not_only_special_character(value):
    if not any(char.isalnum() for char in value):
        raise ValidationError("Field should not contain only special characters.")


def validate_not_only_integer(value):
    if value.isdigit():
        raise ValidationError("Field should not contain only integers.")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password, validate_password_no_spaces],
                                     required=False)
    email = serializers.EmailField(
        error_messages={'blank': 'Email may not be left blank.', 'required': 'Email is required.'})
    full_name = serializers.CharField(
        error_messages={'blank': 'Full name may not be left blank.', 'required': 'Full name is required.'})
    token = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, email):
        try:
            user = User.objects.filter(email=email).first()
            if user is not None:
                raise ValueError('User already exists with this email')
            return email
        except Exception as e:
            raise ValidationError(e)

    def validate(self, data):
        if 'full_name' in data:
            validate_not_only_spaces(data['full_name'])
            validate_not_only_special_character(data['full_name'])
            validate_not_only_integer(data['full_name'])
        return data


    def get_token(self, obj):
        # Use the user's email and password to sign in and get tokens
        data = sign_in(obj.email, self.validated_data['password'])

        # Add 'token' field to the new instance
        token = {
            'access_token': data['access_token'],
            'refresh_token': data['refresh_token']
        }
        return token

    @transaction.atomic
    def create(self, validated_data):
        try:
            password = validated_data.pop('password', None)

            # Create the User instance
            user_instance = self.Meta.model(**validated_data)
            if password is not None:
                user_instance.set_password(password)
                user_instance.save()

            return user_instance
        except Exception as e:
            raise ValidationError(e)


class MeViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            'password': {'write_only': True},
        }


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'access_token',
            'refresh_token',
        )

    def create(self, validated_data):
        data = sign_in(**validated_data)
        return {
            'access_token': data['access_token'],
            "refresh_token": data['refresh_token']
        }


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'code',
        )

    def create(self, validated_data):
        data = reset_code(**validated_data)
        return data


class ResetPasswordSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password, validate_password_no_spaces],
                                     required=False)
    confirm_password = serializers.CharField(write_only=True,
                                             validators=[validate_password, validate_password_no_spaces],
                                             required=False)

    class Meta:
        model = User
        fields = (
            'code',
            'password',
            'confirm_password',
        )

    def create(self, validated_data):
        data = reset_password(**validated_data)
        return Response({"message": "Password Reset Successfully"})


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, error_messages={
        'blank': 'Please enter your current password!'
    })
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, error_messages={
        'blank': 'Please enter a new password!'
    })
