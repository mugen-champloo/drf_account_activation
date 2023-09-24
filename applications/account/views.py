from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from applications.account.serializers import RegisterSerializer
from rest_framework.response import Response

User = get_user_model()


class RegisterApiView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегестрировались', status=201)


class ActivationApiView(APIView):
    @staticmethod
    def get(request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'успещно'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'неверный код'}, status=status.HTTP_400_BAD_REQUEST)

class QuerysetAPI(APIView):
    def get(self, request):
        lst = User.objects.all().values()
        return Response({'users': list(lst)})