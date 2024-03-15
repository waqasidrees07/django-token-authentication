from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .models import *
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from .emails import send_my_email
import random
def sign_in(email, password):
    try:
        user = authenticate(username=email.lower(), password=password)
        
    except User.DoesNotExist:
        raise ValueError("This email address is not registered!")
    except Exception as e:
        raise ValidationError(e)
    if not user.check_password(password):
        raise ValueError("Please enter the correct password.")
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return {"refresh_token":str(refresh),"access_token": str(refresh.access_token)}
    else:
        raise ValueError("Invalid Credentials")


def verification_code():
    return random.randint(1000, 9999)


def reset_code(email):
    try:
        user = User.objects.filter(email=email.lower()).first()
        if user:
            try:
                reset_code = ResetCode.objects.get(user=user)
                reset_code.code = verification_code()
                code = reset_code.code
                reset_code.save()
            except:
                new_code = verification_code()
                reset_code = ResetCode(
                    user=user,
                    code=new_code
                )
                reset_code.save()
                code = reset_code.code
        else:
            raise ValueError('User does not exist with this email')
        email_confirm = send_my_email(email,'reset code', code)
        print('email>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', email_confirm)
        if email_confirm == True:
            return Response({'message':'Check your email for code verification'})
        else:
           raise ValueError('Something went wrong with email confirmation')
    except Exception as e:
        raise ValidationError(e)

    

def reset_password(code, password, confirm_password):
    try:
        reset_code = ResetCode.objects.filter(code=code).first()
        if reset_code is None:
            raise ValueError('The code has expired. Please use a valid code.')
        if password != confirm_password:
                raise ValueError('Password does not match')
        reset_code.user.password = make_password(password)
        reset_code.user.save()
        reset_codes = ResetCode.objects.filter(user=reset_code.user)
        reset_codes.delete()
        return {'message':'Your password has been updated'}
                  
    except Exception as e:
        raise ValidationError(e)