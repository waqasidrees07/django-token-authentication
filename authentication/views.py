from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


# Create your views here.

class SignUpView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer


class SignInView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = SignInSerializer


class UserAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = MeViewSerializer

    def get_object(self):
        try:
            return User.objects.filter(id=self.request.user.id).first()
        except Exception as e:
            raise ValidationError('User does not exists')


class UserPatchAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request):
        user = request.user
        data = request.data

        # Update name and password
        if 'full_name' in data:
            user.full_name = data['full_name']

        if 'password' in data:
            user.password = make_password(data['password'])
        user.save()
        return Response({'message': 'User information updated successfully'}, status=status.HTTP_200_OK)


class ForgotPassword(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ForgotPasswordSerializer


class ResetPassword(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ResetPasswordSerializer


class PasswordUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data["old_password"]
            if not user.check_password(current_password):
                # return Response({"error": "Current password is incorrect", "success": False,}, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(
                    {"error": "Current password is incorrect", "success": False},
                    status=400
                )

            new_password = serializer.validated_data["new_password"]
            user.set_password(new_password)
            user.save()
            response_data = {
                "success": True,
                "message": "Password updated successfully!",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        response_data = {
            "success": False,
            "error": next(iter(serializer.errors.values()))[0],
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
